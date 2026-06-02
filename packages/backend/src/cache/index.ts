import Redis from 'ioredis';
import config from '../config/index.js';

const redis = new Redis(config.redisUrl);

redis.on('connect', () => console.log('[Redis] Connected'));
redis.on('error', (err) => console.error('[Redis] Error:', err));

export default redis;