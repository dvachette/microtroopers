import { WebSocketServer, WebSocket } from 'ws';
import { Server, IncomingMessage } from 'http';
import { ClientMessage } from '@microtroopers/shared/src';
import { handleMessage } from './handlers';
import { parse } from 'cookie';
import jwt from 'jsonwebtoken';
import config from '../config';
import prisma from '../db';

export type Client = {
    ws: WebSocket;
    userId: string;
    pseudo: string;
    roomId: string | null;
};

const clients = new Map<WebSocket, Client>();

export const getClient = (ws: WebSocket): Client | undefined => clients.get(ws);
export const getClients = (): Map<WebSocket, Client> => clients;

const extractUserId = (req: IncomingMessage): { userId: string; } | null => {
    const cookieHeader = req.headers.cookie;
    if (!cookieHeader) return null;

    const cookies = parse(cookieHeader);
    const token = cookies['access_token'];
    if (!token) return null;

    try {
        const payload = jwt.verify(token, config.jwtSecret) as { userId: string };
        return { userId: payload.userId };
    } catch {
        return null;
    }
};

export const initWS = (server: Server): void => {
    const wss = new WebSocketServer({ server });

    wss.on('connection', (ws: WebSocket, req: IncomingMessage) => {
        const auth = extractUserId(req);

        if (!auth) {
            ws.close(4001, 'Unauthorized');
            return;
        }

        const client: Client = { ws, userId: auth.userId, pseudo: '', roomId: null };
        clients.set(ws, client);

        console.log(`[WS] Client connected: ${auth.userId}`);


        // Récupérer le pseudo en async
        prisma.utilisateur.findUnique({
            where: { id: auth.userId },
            select: { pseudo: true },
        }).then(user => {
            if (!user) { ws.close(4002, 'User not found'); return; }
            client.pseudo = user.pseudo;
        }).catch(() => ws.close(4003, 'DB error'));


        ws.on('message', (data) => {
            try {
                const message: ClientMessage = JSON.parse(data.toString());
                handleMessage(client, message);
            } catch {
                console.error('[WS] Invalid message format');
            }
        });

        ws.on('close', () => {
            console.log(`[WS] Client disconnected: ${auth.userId}`);
            clients.delete(ws);
        });

        ws.on('error', (err) => {
            console.error(`[WS] Error for ${auth.userId}:`, err);
        });
    });

    console.log('[WS] WebSocket server initialized');
};

export const sendTo = (client: Client, message: object): void => {
    if (client.ws.readyState === WebSocket.OPEN) {
        client.ws.send(JSON.stringify(message));
    }
};

export const broadcast = (roomId: string, message: object): void => {
    for (const client of clients.values()) {
        if (client.roomId === roomId) {
            sendTo(client, message);
        }
    }
};