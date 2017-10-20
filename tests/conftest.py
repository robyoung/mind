import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlalchemy

from mind.app import create_app, db, get_config
from mind.models import Question


@pytest.fixture(scope='session')
def test_db():
    config = get_config('test')
    db_name = config['DB_DATABASE']
    db_uri = config['SQLALCHEMY_DATABASE_URI']
    db_uri = '/'.join(db_uri.split('/')[:-1])

    engine = sqlalchemy.create_engine(db_uri)
    engine.raw_connection().set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    engine.execute(f'drop database if exists {db_name}')
    engine.execute(f'create database {db_name}')

    yield

    engine.execute(f'''
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{db_name}'
            AND pid <> pg_backend_pid();
    ''')
    engine.execute(f'drop database if exists {db_name}')


@pytest.fixture
def flask_app(test_db):
    app = create_app('test')
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def test_client(flask_app):
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def question(flask_app):
    with flask_app.app_context():
        question = Question(title='Test question')
        db.session.add(question)
        db.session.commit()
    yield question
