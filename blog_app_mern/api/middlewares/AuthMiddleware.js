import models from '../models/UserModel.js';
const { usermodel } = models;
import dotenv from 'dotenv';
import jwt from 'jsonwebtoken';

dotenv.config(); 

const userVerification = async (req, res, next) => {
  const token = req.cookies.token;
  if (!token) {
    return res.status(401).json({ status: false, message: "No token provided" });
  }
  try {
    const decoded = jwt.verify(token, process.env.TOKEN_KEY);
    const user = await usermodel.findById(decoded.id);
    if (!user) {
      return res.status(404).json({ status: false, message: "User not found" });
    }
    req.user = user;
    next(); 
  } catch (err) {
    if (err.name === "JsonWebTokenError") {
      return res.status(401).json({ status: false, message: "Invalid token" });
    } else if (err.name === "TokenExpiredError") {
      return res.status(401).json({ status: false, message: "Token expired" });
    } else {
      return res.status(500).json({ status: false, message: "Internal Server Error" });
    }
  }
}

export default userVerification;

