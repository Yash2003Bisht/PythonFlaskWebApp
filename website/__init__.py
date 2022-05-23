"""
There is a __init__.py file in the website directory, so that python can take this directory as a package
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY']= "$UFHA867863HJgfssaHdsFf4df65s6fas433445!@#$%^&*("
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def NoteApp():
    """Responsible for creating database with models"""
    db.init_app(app)
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    from .models import UserNotes, UserData 
    createDatabase(app)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # were user have go if user were not login
    login_manager.init_app(app)  # here we specify the app

    @login_manager.user_loader
    def load_user(id):
        return UserData.query.get(int(id))

    return app


def createDatabase(app):
    """Creating database if not exists"""
    if not os.path.exists("website/database.db"):
        db.create_all(app=app)