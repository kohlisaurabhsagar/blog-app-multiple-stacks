from flask import Flask
from app.extensions import db
from app.blueprints import user, blogpost
from app.models.usermodel import User
import os
from datetime import timedelta
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect



app = Flask (__name__)
app.secret_key = 'flasksecretkey'
csrf = CSRFProtect(app)

app.config['UPLOAD_FOLDER'] = './app/media'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])



app.permanent_session_lifetime = timedelta(minutes = 30)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/blogapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userapp.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

migrate = Migrate(app, db)




app.register_blueprint(user.bp)
app.register_blueprint(blogpost.bp)


def inject_csrf_token():
    from flask_wtf import generate_csrf
    return dict(csrf_token=generate_csrf())

with app.app_context():
    db.create_all()



