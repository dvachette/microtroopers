import { GameState, GamePhase, Worm, Projectile, LobbyPlayer } from '@microtroopers/shared';
import { broadcast } from '../ws/index';
import { randomUUID } from 'crypto';

const TICK_RATE = 20; // ms
const MAX_PLAYERS = 6;

export class Room {
    readonly id: string;
    private phase: GamePhase = 'waiting';
    private tick: number = 0;
    private interval: NodeJS.Timeout | null = null;

    private players: Map<string, LobbyPlayer> = new Map();
    private worms: Map<string, Worm> = new Map();
    private projectiles: Map<string, Projectile> = new Map();
    private mapWidth: number = 2000;
    private mapHeight: number = 1000;
    private mapData: Buffer | null = null; // bitmap autoritaire serveur

    constructor() {
        this.id = randomUUID();
    }

    // --- Lobby ---

    addPlayer(userId: string, pseudo: string, team: number | null = null): boolean {
        if (this.players.size >= MAX_PLAYERS || this.phase !== 'waiting') return false;

        this.players.set(userId, { userId, pseudo, ready: false, team });
        this.broadcastLobbyState();
        return true;
    }

    removePlayer(userId: string): void {
        this.players.delete(userId);
        this.worms.delete(userId);

        if (this.phase === 'playing' && this.players.size === 0) {
            this.stop();
        } else {
            this.broadcastLobbyState();
        }
    }

    setReady(userId: string, ready: boolean): void {
        const player = this.players.get(userId);
        if (!player) return;
        player.ready = ready;

        if (this.allReady()) this.start();
        else this.broadcastLobbyState();
    }

    private allReady(): boolean {
        if (this.players.size < 2) return false;
        return [...this.players.values()].every(p => p.ready);
    }

    // --- Game lifecycle ---

    private start(): void {
        this.phase = 'starting';
        this.tick = 0;
        this.initWorms();
        this.generateMap();

        broadcast(this.id, {
            type: 'game_start',
            matchId: this.id,
            mapWidth: this.mapWidth,
            mapHeight: this.mapHeight,
            mapData: this.mapData!.toString('base64'),
        });

        this.phase = 'playing';
        this.interval = setInterval(() => this.update(), TICK_RATE);
    }

    stop(): void {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
        this.phase = 'ended';
    }

    // --- Game loop ---

    private update(): void {
        this.tick++;
        this.updateProjectiles();
        this.checkDeaths();
        this.broadcastGameState();
    }

    // --- Physics (stubs) ---

    private updateProjectiles(): void {
        // TODO: physique des projectiles (gravité, collisions bitmap, explosions)
    }

    private checkDeaths(): void {
        for (const [userId, worm] of this.worms) {
            if (worm.health <= 0 && worm.state !== 'dead') {
                worm.state = 'dead';
                broadcast(this.id, { type: 'player_died', userId, killedBy: null });
            }
        }

        const alive = [...this.worms.values()].filter(w => w.state !== 'dead');
        if (alive.length <= 1) {
            const winner = alive[0] ?? null;
            broadcast(this.id, {
                type: 'game_over',
                winnerId: winner?.userId ?? null,
                winningTeam: null,
                stats: [],
            });
            this.stop();
        }
    }

    // --- Inputs ---

    applyInput(userId: string, input: {
        moveLeft: boolean;
        moveRight: boolean;
        jump: boolean;
        aimAngle: number;
        shoot: boolean;
        useItem: boolean;
    }): void {
        // TODO: appliquer l'input au worm correspondant
        const worm = this.worms.get(userId);
        if (!worm || worm.state === 'dead') return;
    }

    selectWeapon(userId: string, itemId: string): void {
        const worm = this.worms.get(userId);
        if (!worm) return;
        worm.equippedWeapon = itemId;
    }

    // --- Init ---

    private initWorms(): void {
        let x = 200;
        for (const player of this.players.values()) {
            this.worms.set(player.userId, {
                userId: player.userId,
                pseudo: player.pseudo,
                position: { x, y: 100 },
                velocity: { x: 0, y: 0 },
                health: 100,
                state: 'idle',
                equippedWeapon: null,
                team: player.team,
            });
            x += 300;
        }
    }

    private generateMap(): void {
        // TODO: génération procédurale
        // Pour l'instant bitmap vide (tout destructible)
        const size = Math.ceil((this.mapWidth * this.mapHeight) / 8);
        this.mapData = Buffer.alloc(size, 0xff); // tous les bits à 1 = terrain plein
    }

    // --- Broadcast ---

    private broadcastLobbyState(): void {
        broadcast(this.id, {
            type: 'lobby_state',
            matchId: this.id,
            players: [...this.players.values()],
        });
    }

    private broadcastGameState(): void {
        const state: GameState = {
            matchId: this.id,
            phase: this.phase,
            tick: this.tick,
            worms: [...this.worms.values()],
            projectiles: [...this.projectiles.values()],
        };
        broadcast(this.id, { type: 'game_state', state });
    }

    // --- Getters ---

    getPhase(): GamePhase { return this.phase; }
    getPlayerCount(): number { return this.players.size; }
    hasPlayer(userId: string): boolean { return this.players.has(userId); }
    isFull(): boolean { return this.players.size >= MAX_PLAYERS; }
}