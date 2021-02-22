import flask
import pytest
from app import create_app
from app.models import Account

# Test all view functions in the app/views.py file
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client # this is where the testing happens!

# Test new account set-up
@pytest.fixture(scope='module')
def new_account():
    account = Account('matt', 'mgriffes@example.com', '123', 'aapl')
    return account