import { Room } from './Room';

class RoomManager {
    private rooms: Map<string, Room> = new Map();

    create(): Room {
        const room = new Room();
        this.rooms.set(room.id, room);
        console.log(`[RoomManager] Room created: ${room.id}`);
        return room;
    }

    get(roomId: string): Room | undefined {
        return this.rooms.get(roomId);
    }

    delete(roomId: string): void {
        this.rooms.delete(roomId);
        console.log(`[RoomManager] Room deleted: ${roomId}`);
    }

    findAvailable(): Room | null {
        for (const room of this.rooms.values()) {
            if (room.getPhase() === 'waiting' && !room.isFull()) return room;
        }
        return null;
    }

    getAll(): Room[] {
        return [...this.rooms.values()];
    }
}

export const roomManager = new RoomManager();