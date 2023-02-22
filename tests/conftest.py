import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # Creates temporary folder to store the database for testing.
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Initializes the DB and runs the script on _data_sql.
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    # Yields the app variable so it can be passed to other fixtures in this code.
    # and also allows for the database cleanup to happen
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    # test_client() is a Flask function that tests fake HTTP responses
    return app.test_client()

@pytest.fixture
def runner(app):
    # test_cli_runner() allows Flask to test CLI commands
    return app.test_cli_runner()
