import express from 'express';
import cookieParser from 'cookie-parser';
import authRouter from './api/auth';

const app = express();

app.use(express.json());
app.use(cookieParser());

app.use('/auth', authRouter);

const PORT = 3020;
app.listen(PORT, () => {
  console.log(`[Server] Running on port ${PORT}`);
});