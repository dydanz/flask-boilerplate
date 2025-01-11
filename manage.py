#!/usr/bin/env python
import os
import sys
import coverage
from flask_migrate import Migrate
from flask import current_app
from marketplace import create_app, db

COV = coverage.coverage(config_file='.coveragerc')

environ = None
if sys.argv[1] in ['cov', 'test']:
    environ = os.getenv('FLASK_CONFIG') or 'test'
    if sys.argv[1] == 'cov':
        COV.start()
else:
    environ = os.getenv('FLASK_CONFIG') or 'development'

app = create_app(environ)
migrate = Migrate(app, db)

def init_db():
    """Initialize the database with a test user."""
    from marketplace.persistence.model import User
    from sqlalchemy import exc

    user = User()
    user.username = 'john_doe_1945'
    user.fullname = 'John Doe'
    user.password = 'this15secret'
    user.phone = '+6280123456789'
    try:
        user.save()
        print('Test user created successfully')
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print('Failed to Create First User:', e)

@app.cli.command("init-db")
def init_db_command():
    """Create test user via Flask CLI."""
    init_db()
    print('Initialized the database.')

@app.cli.command("test")
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command("cov")
def coverage_report():
    """Run the unit tests with coverage."""
    import unittest
    COV.start()
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    COV.html_report()
    COV.erase()
    return 0

if __name__ == '__main__':
    app.run()
