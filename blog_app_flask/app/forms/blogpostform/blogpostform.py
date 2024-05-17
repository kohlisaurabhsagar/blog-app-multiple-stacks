from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileAllowed
from flask_wtf import FlaskForm



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Add Comment')


class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update Post')
