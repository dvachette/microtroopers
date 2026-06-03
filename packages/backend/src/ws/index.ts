import { WebSocketServer, WebSocket } from 'ws';
import { Server } from 'http';
import { ClientMessage } from '@microtroopers/shared/src';
import { handleMessage } from './handlers';

export type Client = {
    ws: WebSocket;
    userId: string;
    roomId: string | null;
};

const clients = new Map<WebSocket, Client>();

export const getClient = (ws: WebSocket): Client | undefined => clients.get(ws);
export const getClients = (): Map<WebSocket, Client> => clients;

export const initWS = (server: Server): void => {
    const wss = new WebSocketServer({ server });

    wss.on('connection', (ws: WebSocket, req) => {
        // TODO: extraire userId depuis le cookie JWT à la connexion
        const userId = 'anonymous'; // remplacé après auth WS

        const client: Client = { ws, userId, roomId: null };
        clients.set(ws, client);

        console.log(`[WS] Client connected: ${userId}`);

        ws.on('message', (data) => {
            try {
                const message: ClientMessage = JSON.parse(data.toString());
                handleMessage(client, message);
            } catch {
                console.error('[WS] Invalid message format');
            }
        });

        ws.on('close', () => {
            console.log(`[WS] Client disconnected: ${userId}`);
            clients.delete(ws);
        });

        ws.on('error', (err) => {
            console.error(`[WS] Error for ${userId}:`, err);
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