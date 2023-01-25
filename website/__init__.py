from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "employees.db"
        
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website / ' + DB_NAME):
        db.create_all(app=app)

