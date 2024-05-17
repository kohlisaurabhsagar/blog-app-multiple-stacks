import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';

dotenv.config(); 


const createSecretToken = (id) => {
  if (!process.env.TOKEN_KEY) {
    throw new Error('TOKEN_KEY must be set in the environment.');
  }
  return jwt.sign({ id }, process.env.TOKEN_KEY, {
    expiresIn: 3 * 24 * 60 * 60, // Expiration time in seconds (3 days)
  });
};

export default createSecretToken;
