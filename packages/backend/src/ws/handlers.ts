import { ClientMessage } from '@microtroopers/shared/src';
import { Client, sendTo } from './index';
import { roomManager } from '../game/RoomManager';

export const handleMessage = (client: Client, message: ClientMessage): void => {
    switch (message.type) {
        case 'join_lobby':
            handleJoinLobby(client, message);
            break;
        case 'leave_lobby':
            handleLeaveLobby(client);
            break;
        case 'player_input':
            handlePlayerInput(client, message);
            break;
        case 'select_weapon':
            handleSelectWeapon(client, message);
            break;
        default:
            sendTo(client, { type: 'error', code: 'UNKNOWN_MESSAGE', message: 'Unknown message type' });
    }
};

const handleJoinLobby = (client: Client, message: Extract<ClientMessage, { type: 'join_lobby' }>): void => {
    let room = roomManager.get(message.matchId) ?? roomManager.findAvailable();

    if (!room) room = roomManager.create();

    const joined = room.addPlayer(client.userId, client.pseudo); // pseudo à récupérer depuis DB
    if (!joined) {
        sendTo(client, { type: 'error', code: 'ROOM_FULL', message: 'Room is full or already started' });
        return;
    }

    client.roomId = room.id;
};

const handleLeaveLobby = (client: Client): void => {
    if (!client.roomId) return;
    const room = roomManager.get(client.roomId);
    if (!room) return;

    room.removePlayer(client.userId);
    client.roomId = null;

    if (room.getPlayerCount() === 0) roomManager.delete(room.id);
};

const handlePlayerInput = (client: Client, message: Extract<ClientMessage, { type: 'player_input' }>): void => {
    if (!client.roomId) return;
    const room = roomManager.get(client.roomId);
    room?.applyInput(client.userId, message.input);
};

const handleSelectWeapon = (client: Client, message: Extract<ClientMessage, { type: 'select_weapon' }>): void => {
    if (!client.roomId) return;
    const room = roomManager.get(client.roomId);
    room?.selectWeapon(client.userId, message.itemId);
};