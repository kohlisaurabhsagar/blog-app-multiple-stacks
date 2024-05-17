import mongoose, { Schema } from 'mongoose';

const postSchema = new Schema({
    title: { type: String, required: true, maxlength: 100 },
    content: { type: String, required: true },
    image: { type: String, maxlength: 255 },
    author: { type: Schema.Types.ObjectId, ref: 'users', required: true },
    dateCreated: { type: Date, default: Date.now },
    comments: [{ type: Schema.Types.ObjectId, ref: 'Comment' }]
});

postSchema.virtual('commentCount').get(function () {
    return this.comments.length;
});

const commentSchema = new Schema({
    user: { type: Schema.Types.ObjectId, ref: 'users', required: true },
    post: { type: Schema.Types.ObjectId, ref: 'Post', required: true },
    content: { type: String, required: true, maxlength: 200 },
    dateCreated: { type: Date, default: Date.now }
});

postSchema.pre('remove', function(next) {
    this.model('Comment').deleteMany({ post: this._id }, next);
});

commentSchema.pre('remove', function(next) {
    this.model('Post').updateOne({ _id: this.post }, { $pull: { comments: this._id } }, next);
});

const Post = mongoose.model('Post', postSchema);
const Comment = mongoose.model('Comment', commentSchema);

export { Post, Comment };

