from app.extensions import db
from datetime import datetime
from app.models.usermodel import User

class PostModel(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def comment_count(self):
        return len(self.comments)

    def __repr__(self):
        return f'<Post {self.title}>'


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref=db.backref('user_comments', lazy=True, cascade="all, delete"))
    post = db.relationship('PostModel', backref=db.backref('comments', lazy='dynamic', cascade="all, delete"))

    def __repr__(self):
        return f'<Comment {self.content}>'
