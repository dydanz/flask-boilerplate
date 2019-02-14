#!/usr/bin/env python
import configparser

from marketplace import create_app

config = configparser.ConfigParser()
config.read(r'module.def')

_app_name = config.get('flask-module', 'module_name')

app = create_app(config.get('flask-module', 'env_name') or 'default')


if __name__ == '__main__':
    app.run()
