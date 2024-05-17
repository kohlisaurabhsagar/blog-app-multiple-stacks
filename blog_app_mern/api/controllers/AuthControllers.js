import models from '../models/UserModel.js';
import createSecretToken from '../utils/secretoken.js'
const { usermodel } = models;
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';



const Register = async (req, res) => {
  try {
    const { username, firstname, lastname, email, password } = req.body;
    const existingUser = await usermodel.findOne({ username });
    if (existingUser) {
      return res.status(409).json({ message: "User already exists" });
    }
    const newuser = new usermodel({
      username,
      firstname,
      lastname,
      email,
      password
    });
    await newuser.save();
    const token = createSecretToken(newuser._id); 
    res.cookie("token", token, { httpOnly: true });
    res.status(201).json({ message: "User signed in successfully", success: true, username: newuser.username });
  } catch (error) {
    console.error("Error during registration:", error);
    res.status(500).json({ success: false, message: "Internal Server Error: " + error.message });
  }
};



const Login = async (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json({ message: 'All fields are required' });
    }
    
    const user = await usermodel.findOne({ username: username });
    if (!user) {
      return res.status(401).json({ message: 'Incorrect username or password' });
    }
    
    const auth = await bcrypt.compare(password, user.password);
    if (!auth) {
      return res.status(401).json({ message: 'Incorrect username or password' });
    }
    
    const token = jwt.sign({ id: user._id }, process.env.TOKEN_KEY, { expiresIn: '2h' });
    
    res.cookie("token", token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production", 
    });

    
    res.status(200).json({
      message: "User logged in successfully",
      success: true,
      token: token, 
      username: user.username,
      email: user.email,
      fname: user.firstname || '',
      lname: user.lastname || '',
      profileImageUrl: user.profileImageUrl || 'default.jpg'
    });
    
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Internal Server Error", success: false });
  }
};


const Logout = (req, res) => {
  res.cookie('token', '', {
    httpOnly: true,   
    expires: new Date(0) 
  });

  res.status(200).json({ message: 'Logout successful' });
};

export {Register,Login, Logout}



