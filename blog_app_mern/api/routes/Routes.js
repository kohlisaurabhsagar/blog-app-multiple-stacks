import express from 'express';
import { Register, Login, Logout } from '../controllers/AuthControllers.js';
import {
    getDashboard,
    createPost,
    serveMedia,
    editPost,
    deletePost,
    upload,
    getComments,
    addComment
} from '../controllers/BlogpostController.js';
import userVerification from '../middlewares/AuthMiddleware.js';
const router = express.Router();

router.post("/signup", Register);
router.post("/login", Login);
router.post("/logout", Logout);
router.use(userVerification);


router.get('/dashboard', userVerification, getDashboard);
router.post('/dashboard', userVerification, upload.single('image'), createPost);
router.get('/media/:filename', userVerification, serveMedia);
router.post('/post/:id/comment', userVerification, addComment);
router.get('/post/:id/comment', userVerification, getComments);
router.put('/post/:id', userVerification, editPost);
router.delete('/post/:id', userVerification, deletePost);

export default router;
