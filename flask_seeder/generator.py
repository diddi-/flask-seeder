""" Generators module """

import random
import pkg_resources

def resource_path(path):
    """ Get the resource path

    Arguments:
        path: Relative path to the resource

    Returns:
        Returns the full filesystem path to the resource.
        Note that no validation is made to ensure the resource actually exist.
    """
    return pkg_resources.resource_filename("flask_seeder", "data/" + path)

def read_resource(path):
    """ Read resource text file

    Reads resource text file and returns content as a list.

    Arguments:
        path: The resource path relative to the data root directory

    Returns:
        A list with the file contents.
    """
    lines = []
    with open(resource_path(path)) as source:
        lines = source.read().splitlines()

    return lines

# pylint: disable=too-few-public-methods
class Generator:
    """ Base Generator class

    Subclasses of Generator must implement the generate() method.

    Attributes:
        rnd: Access to python built-in random module
    """
    def __init__(self, rnd=None):
        self.rnd = rnd or random

    def generate(self):
        """ Generate data
        Must be implemented by subclasses
        """
        raise NotImplementedError()


# pylint: disable=too-few-public-methods
class Integer(Generator):
    """ Random Integer generator """

    def __init__(self, start=1, end=100, **kwargs):
        """ Initialize generator

        Arguments:
            start: Minimum value
            end: Maximum value

        """
        super().__init__(**kwargs)
        self.start = start
        self.end = end

    def generate(self):
        """ Generate a random integer

        Set the start/end attributes prior to calling this method.

        Returns:
            A single random integer from `start` to `end`.
        """
        return self.rnd.randint(self.start, self.end)


# pylint: disable=too-few-public-methods
class Name(Generator):
    """ Random Name generator """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        """ Generate a random name

        Returns:
            A random name in string format
        """
        if self._lines is None:
            self._lines = read_resource("names/names.txt")

        result = self.rnd.choice(self._lines)

        return result
