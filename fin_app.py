from app import create_app, db
from app.models import Account
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Account=Account)

# Just playing with testing here...
@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=False)