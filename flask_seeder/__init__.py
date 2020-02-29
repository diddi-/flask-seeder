""" Flask-Seeder """

from .seeder import Seeder
from .faker import Faker

# pylint: disable=too-few-public-methods
class SeedConfig:
    """ Seed config stored in Flask

    This is intended to be stored as an instance inside a Flask app
    for access to Flask-Seed configuration.
    """
    def __init__(self, db):
        self.db = db


# pylint: disable=too-few-public-methods
class FlaskSeeder:
    """ Flask extension Flask-Seeder

    Usage:
        seeder = FlaskSeeder()
        seeder.init_app(app, db)

    """
    def __init__(self, app=None, db=None):
        """ Initialize FlaskSeeder
        Arguments:
            app: Flask app
            db: SQLAlchemy database object
        """
        self.app = app
        self.db = db

        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        """ Initialize app after construction

        Initialize Flask-Seeder and register as an extension with Flask

        Arguments:
            app: Flask app
            db: SQLAlchemy database object

        """
        self.db = db or self.db

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['flask_seeder'] = SeedConfig(self.db)
