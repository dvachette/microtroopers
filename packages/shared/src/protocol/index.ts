import type { GameState, LobbyPlayer } from '../types/index.js';

// Client → Serveur
export type PlayerInput = {
  moveLeft: boolean;
  moveRight: boolean;
  jump: boolean;
  aimAngle: number;
  shoot: boolean;
  useItem: boolean;
};

export type C2S_JoinLobby = {
  type: 'join_lobby';
  matchId: string;
};

export type C2S_LeaveLobby = {
  type: 'leave_lobby';
};

export type C2S_PlayerInput = {
  type: 'player_input';
  tick: number;
  input: PlayerInput;
};

export type C2S_SelectWeapon = {
  type: 'select_weapon';
  itemId: string;
};

export type ClientMessage =
  | C2S_JoinLobby
  | C2S_LeaveLobby
  | C2S_PlayerInput
  | C2S_SelectWeapon;

// Serveur → Client
export type S2C_LobbyState = {
  type: 'lobby_state';
  matchId: string;
  players: LobbyPlayer[];
};

export type S2C_GameStart = {
  type: 'game_start';
  matchId: string;
  mapWidth: number;
  mapHeight: number;
  mapData: string; // bitmap base64 compressé
};

export type S2C_GameState = {
  type: 'game_state';
  state: GameState;
};

export type S2C_Explosion = {
  type: 'explosion';
  x: number;
  y: number;
  radius: number;
};

export type S2C_PlayerDied = {
  type: 'player_died';
  userId: string;
  killedBy: string | null;
};

export type S2C_GameOver = {
  type: 'game_over';
  winnerId: string | null;
  winningTeam: number | null;
  stats: {
    userId: string;
    kills: number;
    deaths: number;
    placement: number;
  }[];
};

export type S2C_Error = {
  type: 'error';
  code: string;
  message: string;
};

export type ServerMessage =
  | S2C_LobbyState
  | S2C_GameStart
  | S2C_GameState
  | S2C_Explosion
  | S2C_PlayerDied
  | S2C_GameOver
  | S2C_Error;