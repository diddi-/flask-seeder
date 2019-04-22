""" Generators module """

import random
import pkg_resources

from flask_seeder.parser import SGParser, Tokenizer

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

def slicer(string, start, end):
    """ Slice a string

    Return a slice of the string matching anything between, and including,
    the `start` and `end` characters.

    Arguments:
        string: Original string
        start: Start character to begin slicing
        end: End character to stop slicing

    Returns:
        A new string which is a slice from the original string, including the start
        and end characters.

        None is return in case a valid slice couldn't be found, as in start or end
        characters are inversed or doesn't exist in the original slice.
    """
    result = ""
    add = False
    for char in string:
        if char == start:
            add = True
        if add:
            result += char

        # Only return if we have found start
        if char == end and add:
            return result

    return None

# pylint: disable=too-few-public-methods
class Generator:
    """ Base Generator class

    Subclasses of Generator must implement the generate() method.

    Attributes:
        rnd: Access to python built-in random module
        ascii_characters: String with valid ascii characters
        integers: String with valid integers
    """
    def __init__(self, rnd=None):
        self.rnd = rnd or random
        self.alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.digit = "0123456789"

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


class Sequence(Generator):
    """ Sequence integer generator """

    def __init__(self, start=1, end=100, **kwargs):
        """ Initialize generator

        Arguments:
            start: Start of sequence
            end: End of sequence
        """
        super().__init__(**kwargs)
        self._start = start
        self.end = end

        self._next = self.start

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value
        if self._next < self._start:
            self._next = self._start

    def generate(self):
        """ Generate next integer in the sequence

        This method will raise a RuntimeError if the sequence
        has reached the end.
        """
        value = self._next
        self._next += 1

        if value > self.end:
            raise RuntimeError

        return value

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

class String(Generator):
    """ Generate string from pattern

    This generator work by reading a pattern that describes how to
    generate the string.

    The pattern looks like a simplified regular expression but is processed
    completely different, so don't expect normal regular expressions to work.

    See docs for details.
    """

    def __init__(self, pattern=None, parser=None, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.parser = parser or self._create_parser()

    def _create_parser(self): # pylint: disable=no-self-use
        tokenizer = Tokenizer()
        return SGParser(tokenizer=tokenizer)

    def _range(self, quantifier):
        """ Create a range from quantifier

        There are two types of quantifiers

        QUANTIFIER: Repeat X times
        QUANTIFIER_RANGE: Repeat X times, where X is anywhere between start and end

        Returns:
            Python built in range() with a size depending on quantifier type.
        """
        size = 1
        if quantifier["type"] == "QUANTIFIER":
            size = quantifier["value"]
        elif quantifier["type"] == "QUANTIFIER_RANGE":
            start = quantifier["value"]["start"]
            end = quantifier["value"]["end"]
            size = self.rnd.choice(list(range(start, end+1)))

        return range(size)

    def generate_CHARCODE(self, node): # pylint: disable=invalid-name
        """ Generate CHARCODE string

        Generates a string depending on the CHARCODE:
            "c": Character/alpha
            "d": Digit
        """
        result = ""

        for _ in self._range(node["repeat"]):
            if node["value"] == "c":
                result += self.rnd.choice(self.alpha)
            elif node["value"] == "d":
                result += self.rnd.choice(self.digit)
            else:
                raise ValueError("Invalid CHARCODE %s" % node["value"])

        return result

    def generate_ONEOF(self, node): # pylint: disable=invalid-name
        """ Generate one from list

        Returns a value from a list of valid values
        """
        result = ""

        for _ in self._range(node["repeat"]):
            result += self.rnd.choice(node["value"])

        return result

    def generate_RANGE(self, node): # pylint: disable=invalid-name
        """ Generate a range of values

        Generates, in sequence, a number of alpha or digit characters.
        """
        result = ""
        start = node["value"]["start"]
        end = node["value"]["end"]

        source = self.alpha
        if str.isdigit(start):
            source = self.digit

        for _ in self._range(node["repeat"]):
            choices = slicer(source, start, end)
            result += self.rnd.choice(choices)

        return result

    def generate_STRING_GROUP(self, node): # pylint: disable=invalid-name
        """ Generate a string form a list of strings """
        result = ""

        for _ in self._range(node["repeat"]):
            result += self.rnd.choice(node["value"])

        return result

    def generate_NUMBER(self, node): # pylint: disable=invalid-name
        """ Generate number literal """
        result = ""

        for _ in self._range(node["repeat"]):
            result += str(node["value"])

        return result

    def generate_STRING(self, node): # pylint: disable=invalid-name, no-self-use
        """ Generate string literal """
        return node["value"]

    def generate_LITERAL(self, node): # pylint: disable=invalid-name, no-self-use
        """ Generate literal """
        return node["value"]

    def generate(self):
        """ Generate a string based on pattern """
        ast = self.parser.parse(self.pattern)
        result = ""

        for node in ast:
            function_name = "generate_" + node["type"]
            if not hasattr(self, function_name):
                raise NotImplementedError("Unknown node type %s" % node["type"])

            func = getattr(self, function_name)
            result += func(node)

        return result
