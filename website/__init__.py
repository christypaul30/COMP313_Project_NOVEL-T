from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
# DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'professor anders is waifu'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    ENV = 'dev'
    if ENV == 'dev':
        app.debug = True
        print("Using dev server")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/novelt'
    else:
        app.debug = False
        print("Using production server")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yhslrfopruboqu:f8ee68219de833159b732325e940174f7f10bc0138daa17b009dcb745cc13b8a@ec2-44-198-24-0.compute-1.amazonaws.com:5432/d2qbqedi3pjns4'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, CharacterSheet, Book, BookChapters, BookGenres, Library

    # create_database(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def create_database(app):
    db.create_all(app=app)
    print('Database created')
