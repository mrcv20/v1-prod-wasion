from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


db = SQLAlchemy()


python = 3


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'whatever'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:admin123@localhost/teste'
    db.init_app(app)
    Bootstrap(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all(app=app)
        print("Created Database")
    else:
        print("already created")    