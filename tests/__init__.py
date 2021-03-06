import urllib
from unittest import TestCase
from app import application
from app.models import db


class Base(TestCase):
    def setUp(self):
        application.config['RUN_MODE'] = 'test'
        application.config.from_object('app.config.test.Config')

        db.session.close()
        db.drop_all()
        db.create_all()

        self.app = application.test_client(self)
        self.app_context = application.app_context()
        self.app_context.push()

    def api_get(self, path, data=None, version=None):
        options = {}
        url = path + '?' + urllib.parse.urlencode(data) if data else path

        if version:
            options['headers'] = {'X-Api-Version': version}

        return self.app.get(url, **options)
