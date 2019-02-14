import sys
from unittest import TestCase

from marketplace import create_app, db


def run(command_line, manager_run):
    """
        Runs a manager command line, returns exit code
    """
    sys.argv = command_line.split()
    exit_code = None
    try:
        manager_run()
    except SystemExit as e:
        exit_code = e.code

    return exit_code


class BaseTestCase(TestCase):
    def setUp(self):
        app_test = create_app('testing')
        self.client = app_test.test_client()
        self.app_context = app_test.app_context()
        self.app_context.push()

        self.request_context = app_test.test_request_context()
        self.request_context.push()

        with self.app_context:
            db.create_all()

        # Disable Traceback, expect cleaner Test Result log
        sys.tracebacklimit = 1

    def tearDown(self):
        with self.app_context:
            db.session.remove()
            db.drop_all()

        self.request_context.pop()
        self.app_context.pop()
        TestCase.tearDown(self)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class Constants(object):
    PHONE_NUMBER = '+628123456789'
    VERIFICATION_ID = '12345'
    DEVICE_ID = '1234567890'
    PUSH_TOKEN = '1234567890'
    SESSION_ID = '1234567890'
    DEVICE_TYPE_ANDROID = 'android'
    DEVICE_TYPE_IOS = 'ios'
    DEVICE_TYPE_WEB = 'web'
