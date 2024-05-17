import multer from 'multer';
import { Post, Comment } from '../models/BlogpostModel.js';
import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';



const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, './uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

const fileFilter = (req, file, cb) => {
  if (['image/jpeg', 'image/png'].includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Unsupported file type'), false);
  }
};

export const upload = multer({ storage, fileFilter });

export const getDashboard = async (req, res) => {
  if (!req.user) {
    return res.status(401).json({ message: "Unauthorized" });
  }
  try {
    const posts = await Post.find().populate('author').exec();
    res.status(200).json(posts.map(post => ({
      ...post.toObject(), // Convert Mongoose document to a plain JavaScript object
      imageUrl: post.imageUrl,
      authorName: post.author ? post.author.username : 'Unknown' 
    })));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};




export const createPost = async (req, res) => {
  if (!req.user) {
    return res.status(401).json({ message: "Unauthorized" });
  }
  try {
    const { title, content } = req.body;
    const newPost = new Post({
      title,
      content,
      image: req.file ? req.file.filename : undefined,
      author: req.user._id
    });

    await newPost.save();

    const populatedPost = await Post.findById(newPost._id).populate('author', 'username firstname lastname');

    res.status(200).json({ message: 'Post created successfully', post: populatedPost });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};



export const serveMedia = (req, res) => {
  const filename = req.params.filename;
  res.status(200).sendFile(path.resolve('uploads', filename));
};




export const addComment = async (req, res) => {
  if (!req.user) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  const { content } = req.body;
  const newComment = new Comment({
    user: req.user._id,
    post: req.params.id,
    content
  });

  try {
    await newComment.save();
    await newComment.populate({
      path: 'user',
      select: 'username email'
    });

    res.status(201).json({
      message: 'Comment added successfully',
      comment: newComment
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};


export const getComments = async (req, res) => {
  if (!req.user) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  try {
    const comments = await Comment.find({ post: req.params.id })
                                  .populate('user', 'username email');
    res.status(200).json(comments);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

export const editPost = async (req, res) => {
  if (!req.user) {
    return res.status(401).json({ message: "Unauthorized" });
  }
  try {
    const { title, content, image } = req.body;
    const post = await Post.findByIdAndUpdate(req.params.id, {
      title, content, image
    }, { new: true });
    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }
    res.status(200).json({ message: 'Post updated successfully', post });
  } catch (error) {
    res.status(500).json({ message: 'Failed to update post', error: error.message });
  }
};


export const deletePost = async (req, res) => {
  if (!req.user) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  try {
    const post = await Post.findById(req.params.id);
    if (!post) {
      return res.status(404).json({ message: "Post not found" });
    }

    if (post.image) {
      const imagePath = path.join(__dirname, '..', 'uploads', post.image);
      try {
        await fs.unlink(imagePath);
      } catch (err) {
        console.error("Failed to delete image file:", err);
        throw err;
      }
    }

    await Post.findByIdAndDelete(req.params.id);
    res.status(200).json({ message: "Post and image deleted successfully" });
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};
