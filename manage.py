#!/usr/bin/env python
import os
import sys

import coverage
from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from marketplace import create_app

COV = coverage.coverage(config_file='.coveragerc')

environ = None
if sys.argv[1] in ['cov', 'test']:
    environ = os.getenv('FLASK_CONFIG') or 'testing'
    if sys.argv[1] == 'cov':
        COV.start()
else:
    environ = os.getenv('FLASK_CONFIG') or 'default'

app = create_app(environ)
manager = Manager(app)

# Enable us to manage and run flask-app locally
manager.add_command('db', MigrateCommand)
manager.add_command(
        "runserver",
        Server(
                threaded=True,
                use_reloader=manager.app.debug,
                use_debugger=manager.app.debug,
                host='0.0.0.0',
                port=5000,
        )
)


@manager.command
def initdb():
    from marketplace import db
    from sqlalchemy import exc
    from marketplace.persistence.model import User

    user = User()
    user.username = 'john_doe_1945'
    user.fullname = 'John Doe'
    user.password = 'this15secret'
    user.phone = +6280123456789
    try:
        user.save()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print('Failed to Create First User, %s', e)


@manager.command
def cov():
    """Run the unit test with coverage."""
    from marketplace import test

    tests = test.TestLoader().discover('test')
    test.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    COV.html_report()
    COV.erase()
    return 0


@manager.command
def test(coverage=False, test_name=None):
    """Run the unit test.

    To run all test:
        $ python3 manage.py test

    Example of running an individual unit test:
        $ python3 manage.py test -t api.test_cms_v2_routes.CMSApiTestCase

    """
    import unittest

    test_dir = 'marketplace.test'

    if test_name is None:
        tests = unittest.TestLoader().discover(test_dir)
    else:
        tests = unittest.TestLoader().loadTestsFromName(test_dir + '.' + test_name)
    runner = unittest.TextTestRunner(verbosity=2).run(tests)
    sys.exit(not runner.wasSuccessful())


manager.run()
