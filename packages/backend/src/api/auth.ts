import { Router, Request, Response } from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { randomUUID } from 'crypto';
import prisma from '../db';
import redis from '../cache';
import config from '../config';
import { requireAuth, AuthPayload } from '../middleware/auth';

const router = Router();

const SALT_ROUNDS = 12;
const REFRESH_TOKEN_KEY = (token: string) => `session:${token}`;

const generateTokens = (userId: string) => {
  const accessToken = jwt.sign({ userId }, config.jwtSecret, {
    expiresIn: config.jwtExpiresIn,
  });
  const refreshToken = randomUUID();
  return { accessToken, refreshToken };
};

const setAuthCookies = (res: Response, accessToken: string, refreshToken: string) => {
  res.cookie('access_token', accessToken, {
    httpOnly: true,
    secure: config.nodeEnv === 'production',
    sameSite: 'strict',
    maxAge: 15 * 60 * 1000,
  });
  res.cookie('refresh_token', refreshToken, {
    httpOnly: true,
    secure: config.nodeEnv === 'production',
    sameSite: 'strict',
    maxAge: config.refreshTokenTtl * 1000,
  });
};

// POST /auth/register
router.post('/register', async (req: Request, res: Response): Promise<void> => {
  const { pseudo, password } = req.body;

  if (!pseudo || !password) {
    res.status(400).json({ error: 'pseudo and password are required' });
    return;
  }

  if (password.length < 8) {
    res.status(400).json({ error: 'Password must be at least 8 characters' });
    return;
  }

  try {
    const existing = await prisma.utilisateur.findUnique({ where: { pseudo } });
    if (existing) {
      res.status(409).json({ error: 'Pseudo already taken' });
      return;
    }

    const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
    const user = await prisma.utilisateur.create({
      data: { pseudo, passwordHash },
    });

    const { accessToken, refreshToken } = generateTokens(user.id);
    await redis.set(REFRESH_TOKEN_KEY(refreshToken), user.id, 'EX', config.refreshTokenTtl);
    setAuthCookies(res, accessToken, refreshToken);

    res.status(201).json({ userId: user.id, pseudo: user.pseudo });
  } catch {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /auth/login
router.post('/login', async (req: Request, res: Response): Promise<void> => {
  const { pseudo, password } = req.body;

  if (!pseudo || !password) {
    res.status(400).json({ error: 'pseudo and password are required' });
    return;
  }

  try {
    const user = await prisma.utilisateur.findUnique({ where: { pseudo } });
    if (!user || user.deleted) {
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) {
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    const { accessToken, refreshToken } = generateTokens(user.id);
    await redis.set(REFRESH_TOKEN_KEY(refreshToken), user.id, 'EX', config.refreshTokenTtl);
    setAuthCookies(res, accessToken, refreshToken);

    res.status(200).json({ userId: user.id, pseudo: user.pseudo });
  } catch {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /auth/refresh
router.post('/refresh', async (req: Request, res: Response): Promise<void> => {
  const refreshToken = req.cookies?.refresh_token;

  if (!refreshToken) {
    res.status(401).json({ error: 'No refresh token' });
    return;
  }

  try {
    const userId = await redis.get(REFRESH_TOKEN_KEY(refreshToken));
    if (!userId) {
      res.status(401).json({ error: 'Invalid or expired refresh token' });
      return;
    }

    await redis.expire(REFRESH_TOKEN_KEY(refreshToken), config.refreshTokenTtl);

    const newAccessToken = jwt.sign({ userId }, config.jwtSecret, {
      expiresIn: config.jwtExpiresIn,
    });

    res.cookie('access_token', newAccessToken, {
      httpOnly: true,
      secure: config.nodeEnv === 'production',
      sameSite: 'strict',
      maxAge: 15 * 60 * 1000,
    });

    res.status(200).json({ ok: true });
  } catch {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /auth/logout
router.post('/logout', requireAuth, async (req: Request, res: Response): Promise<void> => {
  const refreshToken = req.cookies?.refresh_token;

  if (refreshToken) {
    await redis.del(REFRESH_TOKEN_KEY(refreshToken));
  }

  res.clearCookie('access_token');
  res.clearCookie('refresh_token');
  res.status(200).json({ ok: true });
});

// GET /auth/me
router.get('/me', requireAuth, async (req: Request, res: Response): Promise<void> => {
  const { userId } = res.locals.auth as AuthPayload;

  try {
    const user = await prisma.utilisateur.findUnique({
      where: { id: userId },
      select: {
        id: true,
        pseudo: true,
        balanceGold: true,
        balanceGems: true,
        administrator: true,
      },
    });

    if (!user) {
      res.status(404).json({ error: 'User not found' });
      return;
    }

    res.status(200).json(user);
  } catch {
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;