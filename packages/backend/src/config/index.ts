import dotenv from 'dotenv';
import { resolve } from 'path';

dotenv.config({ path: resolve(__dirname, '../../../../.env') });

const required = (key: string): string => {
    const value = process.env[key];
    if (!value) throw new Error(`Missing environment variable: ${key}`);
    return value;
};

const config = {
    nodeEnv: process.env.NODE_ENV ?? 'development',
    databaseUrl: required('DATABASE_URL'),
    redisUrl: process.env.REDIS_URL ?? 'redis://localhost:6379',
    jwtSecret: required('JWT_SECRET'),
    jwtExpiresIn: '15m',
    refreshTokenTtl: 60 * 60 * 24 * 7, // 7 jours en secondes
} as const;

export default config;