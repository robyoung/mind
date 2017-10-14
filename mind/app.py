import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app(environment):
    app = Flask(__name__)

    app.config.update(get_config(environment))

    db.init_app(app)
    app.migrate = Migrate(app, db)

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
