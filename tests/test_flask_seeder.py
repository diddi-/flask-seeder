from unittest import TestCase
from unittest.mock import MagicMock
from flask_seeder import FlaskSeeder

class TestFlaskSeeder(TestCase):

    def test_init_app_without_db(self):
        """ FlaskSeeder should use db object when passed via constructor.
        """
        db = MagicMock()
        app = MagicMock()
        ext = {}
        app.extensions.__setitem__.side_effect = ext.__setitem__
        seeder = FlaskSeeder(db=db)

        seeder.init_app(app)

        self.assertEqual(ext["flask_seeder"].db, db)
