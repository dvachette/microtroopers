export type Vec2 = { x: number; y: number };

export type WormState = 'idle' | 'moving' | 'jumping' | 'falling' | 'dead';

export type Worm = {
    userId: string;
    pseudo: string;
    position: Vec2;
    velocity: Vec2;
    health: number;
    state: WormState;
    equippedWeapon: string | null;
    team: number | null;
};

export type Projectile = {
    id: string;
    ownerId: string;
    position: Vec2;
    velocity: Vec2;
    itemId: string;
};

export type GamePhase = 'waiting' | 'starting' | 'playing' | 'ended';

export type GameState = {
    matchId: string;
    phase: GamePhase;
    tick: number;
    worms: Worm[];
    projectiles: Projectile[];
};

export type LobbyPlayer = {
    userId: string;
    pseudo: string;
    ready: boolean;
    team: number | null;
};