from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usermodel import User 
from app.forms.userform.userform import RegistrationForm, LoginForm, UserUpdateForm
from app.extensions import db
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired, FileAllowed
import os
from flask_login import login_user, logout_user, current_user, login_required



bp = Blueprint("userapp", __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':

      if form.validate_on_submit():        

          user = User(
              username=form.username.data,
              email=form.email.data,
              fname=form.fname.data,
              lname=form.lname.data,
              password=form.password.data,  
          )

          db.session.add(user)
          db.session.commit()
          flash('Account created successfully! You can now log in.', 'success')
          return redirect(url_for('userapp.login'))

    return render_template('signup.html', form=form)


@bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
      if form.validate_on_submit():
          user = User.query.filter_by(username=form.username.data).first()
          if user and user.check_password(form.password.data):
              login_user(user)
              flash('You have been logged in!', 'success')
              return redirect(url_for('blogpostapp.home')), 200 
          else:
              flash('Login Unsuccessful. Please check username and password', 'danger')
              return redirect(url_for('userapp.login'))
    return render_template('login.html', form=form)

# @bp.route('/user-update/<int:pk>', methods=['GET', 'POST'])
# def user_update(pk):
#     form = UserUpdateForm()
#     user = User.query.filter_by(username=current_user.username).first()
#     if request.method == 'POST' and form.validate_on_submit():
#         image_file = request.files['image']
#         filename = None 
        
#         if image_file and allowed_file(image_file.filename):
#             filename = secure_filename(image_file.filename)
#             filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#             image_file.save(filepath)
          
#           return redirect(url_for('blogpostapp.profile')) 
#       else:
#           flash('Update Failed', 'danger')
#           return redirect(url_for('userapp.user_update'))
#     return render_template('profile.html', form=form)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')




