from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.models.blogpostmodel import *
from app.forms.blogpostform.blogpostform import PostForm, CommentForm, UpdatePostForm
from app.extensions import db
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired, FileAllowed
import os
from flask_login import current_user, login_required
from flask import send_from_directory
from sqlalchemy import desc
from werkzeug.datastructures import ImmutableMultiDict



bp = Blueprint("blogpostapp", __name__)


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def home():
    posts = PostModel.query.all()
    form = PostForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        image_file = request.files['image']
        filename = None 
        for i in form:
            print(i)
        
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            image_file.save(filepath)
        
        new_post = PostModel(
            title=form.title.data,
            content=form.content.data,
            image=filename,  
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post added successfully!', 'success')
        return redirect(url_for('blogpostapp.home', post_id=new_post.id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'error')
    return render_template('index.html', form=form, posts=posts)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

@bp.route('/media/<filename>')
@login_required
def media(filename):
    return send_from_directory('media', filename)



# @bp.route('/post/<int:pk>', methods=['GET', 'POST',  'PUT'])
# @login_required
# def post_details(pk):
#     post = PostModel.query.get_or_404(pk)  
#     comment_form = CommentForm()
    
#     if request.method == 'POST':
#         if comment_form.validate_on_submit():
#             instance = Comments(
#                 user_id=current_user.id,  
#                 post_id=post.id,
#                 content=comment_form.content.data  
#             )
#             db.session.add(instance)
#             db.session.commit()
#             flash('Your comment has been added!', 'success')
#             return redirect(url_for('blogpostapp.post_details', pk=post.id)) 
#         else:
#             flash('Error adding comment.', 'error')
#     return render_template('post_details.html', post=post, comment_form=comment_form)


# @bp.route('/post/<int:pk>/edit', methods=['GET', 'POST'])
# @login_required
# def post_edit(pk):
#     post = PostModel.query.get_or_404(pk)
#     form = UpdatePostForm(obj=post)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             form.populate_obj(post)
#         db.session.commit()
#         flash('Post updated successfully.')
#         return redirect(url_for('blogpostapp.post_details',  pk=post.id))
#     return render_template('post_edit.html', form=form, post=post)


@bp.route('/post/<int:pk>', methods=['GET', 'POST', 'PUT'])
@login_required
def post_details_or_edit(pk):
    post = PostModel.query.get_or_404(pk)
    comment_form = CommentForm()
    edit_form = UpdatePostForm(obj=post)
    if request.method == 'POST' and request.form.get('_method') == 'PUT':
        request.method = 'PUT'
        request.form = ImmutableMultiDict(request.form)

    if request.method == 'POST':
        if comment_form.validate_on_submit():
            comment = Comments(
                user_id=current_user.id,
                post_id=post.id,
                content=comment_form.content.data
            )
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
            return redirect(url_for('blogpostapp.post_details_or_edit', pk=post.id))
        else:
                flash('Error adding comment.', 'error')


    elif request.method == 'PUT':
        if edit_form.validate_on_submit():
            edit_form.populate_obj(post)
            db.session.commit()
            flash('Post updated successfully.', 'success')
            return redirect(url_for('blogpostapp.post_details_or_edit', pk=post.id))
        else:
            flash('Error updating the post.', 'error')

    action = request.args.get('action')
    if action == 'edit':
        return render_template('post_edit.html', form=edit_form, post=post)
    return render_template('post_details.html', post=post, comment_form=comment_form)




@bp.route('/post/<int:pk>/delete', methods=['POST'])
@login_required
def post_delete(pk):
    post = PostModel.query.get_or_404(pk)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.')
    return redirect(url_for('blogpostapp.home'))






