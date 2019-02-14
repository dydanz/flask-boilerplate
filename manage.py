#!/usr/bin/env python
import sys

import coverage
import os
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

manager.run()


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
