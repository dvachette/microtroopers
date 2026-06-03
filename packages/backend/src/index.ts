import 'dotenv/config';
import express from 'express';
import cookieParser from 'cookie-parser';
import { createServer } from 'http';
import authRouter from './api/auth';
import { initWS } from './ws/index';

const app = express();
app.use(express.json());
app.use(cookieParser());

app.use('/auth', authRouter);

const server = createServer(app);
initWS(server);

const PORT = 3020;
server.listen(PORT, () => {
  console.log(`[Server] Running on port ${PORT}`);
});