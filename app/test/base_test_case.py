from flask_testing import TestCase
from app.main import DB
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        DB.create_all()
        DB.session.commit()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()
