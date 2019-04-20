""" Faker module """

from flask_seeder.generator import Generator

# pylint: disable=too-few-public-methods
class Faker:
    """ Base Faker class

    The `init` attribute is a dictionary that tells Faker how to
    initialize the classes, for example:
        {
            "name": generator.Name()
        }

    Attributes:
        cls: The type of class to be created
        init: Dictionary with initialization data
    """

    def __init__(self, cls=None, init=None):
        """ Initialize faker """
        self.cls = cls
        self.init = init

    def _init_args(self):
        args = {}
        if self.init is None:
            return args

        for arg, value in self.init.items():
            if isinstance(value, Generator):
                args[arg] = value.generate()
            else:
                args[arg] = value

        return args

    def create(self, limit=1):
        """ Create objects

        Create a number of instance of `cls`,
        all initialized with data from `init`.

        Arguments:
            limit: How many objects to create, default 1.

        Returns:
            List of `cls` instances initialized with data from `init`.
        """
        instances = []
        for _ in range(limit):
            args = self._init_args()
            instances.append(self.cls(**args))

        return instances
