""" Base seeder """

# pylint: disable=too-few-public-methods
class Seeder:
    """ Base seeder class """

    def __init__(self, db=None):
        self.db = db
        self.name = None
        self.mod_path = None
        self.file_path = None

    def run(self):
        """ Run the seeder script.

        Must be implemented by the client.
        """
        raise NotImplementedError()
