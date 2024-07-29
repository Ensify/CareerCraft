from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_toastr import Toastr
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
toastr = Toastr()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    toastr.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth
    from app.routes.main import main

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    with app.app_context():
        db.create_all()

    return app
