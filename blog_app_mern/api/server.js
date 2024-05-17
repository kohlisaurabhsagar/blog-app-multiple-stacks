import express from "express";
import cors from 'cors';
import dotenv from 'dotenv';
import router from './routes/Routes.js';
import cookieParser from 'cookie-parser';
import dbCon from "./utils/db.js"; 


dotenv.config(); 

const app = express();
dbCon(); 

app.use(express.json());
app.use(cookieParser());
app.use(cors({
  origin: 'http://localhost:3000', // allow to server to accept request from different origin
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true // allow session cookie from browser to pass through
}));
app.use('/uploads', express.static('uploads'));
app.use('/api', router);
app.use((req, res, next) => {
  console.log('Request URL:', req.originalUrl);
  next();
});

app.listen(process.env.PORT, () => {
    console.log(`Server is listening on port ${process.env.PORT}`);
});
