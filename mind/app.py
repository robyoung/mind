import os
import uuid

from flask import Flask, session
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from werkzeug.contrib.fixers import ProxyFix

from .database import db
from .models import User


oauth = OAuth()
google = oauth.remote_app(
    'google',
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_params={
        'scope': 'email'
    },
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    app_key='GOOGLE',
)
login_manager = LoginManager()


def create_app(environment):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.update(get_config(environment))

    db.init_app(app)
    app.migrate = Migrate(app, db)

    oauth.init_app(app)
    login_manager.init_app(app)

    from .blueprints.mind import mind as mind_blueprint
    app.register_blueprint(mind_blueprint, url_prefix='/mind')

    app.add_url_rule('/', view_func=lambda: 'OK')

    return app


def get_config(environment):
    environment = environment.lower()
    assert environment in ["dev", "test", "prod"]

    config = {
        "ENVIRONMENT": environment,
        "SECRET_KEY": os.environ.get("SECRET_KEY", "a big bad secret"),
        "DB_HOST": os.environ.get("DB_HOST", "db"),
        "DB_USER": os.environ.get("DB_USER", "mind"),
        "DB_PASSWORD": os.environ.get("DB_PASSWORD", "mind"),
        "DB_DATABASE": os.environ.get("DB_DATABASE", "mind"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,

        # OAuth
        "GOOGLE_CONSUMER_KEY": os.environ.get("GOOGLE_ID"),
        "GOOGLE_CONSUMER_SECRET": os.environ.get("GOOGLE_SECRET"),

        "EMAIL_HASH_SALT": os.environ["EMAIL_HASH_SALT"],
    }

    if environment == "test":
        config['DB_DATABASE'] = 'test_mind'

    config["SQLALCHEMY_DATABASE_URI"] = _sqlalchemy_uri(
        "postgresql",
        config["DB_USER"], config["DB_PASSWORD"],
        config["DB_HOST"], "5432",
        config["DB_DATABASE"]
    )
    return config


def _sqlalchemy_uri(dialect, username, password, host, port, database):
    return "{dialect}://{username}:{password}@{host}:{port}/{database}".format(
        dialect=dialect,
        username=username, password=password,
        host=host, port=port,
        database=database)


@login_manager.user_loader
def load_user(user_uuid):
    return LoginUser.get(user_uuid)


class LoginUser(UserMixin):
    def __init__(self, user):
        self._user = user

    @staticmethod
    def login(user, info):
        session['user_info'] = {
            k: v for k, v in info.items()
            if k in ['email', 'given_name']
        }
        session.permanent = True
        login_user(LoginUser(user))

    @staticmethod
    def logout():
        logout_user()
        session.pop('user_info', None)

    @staticmethod
    def get(user_uuid):
        try:
            user = User.query.get(uuid.UUID(user_uuid))
            if user:
                return LoginUser(user)
        except ValueError:
            pass

    def get_id(self):
        return str(self._user.uuid)

    @property
    def given_name(self):
        return session['user_info']['given_name']

    @property
    def email(self):
        return session['user_info']['email']

    @property
    def user(self):
        return self._user
