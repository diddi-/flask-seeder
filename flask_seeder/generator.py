""" Generators module """

import re
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

def substr_replace(string, startpos, endpos, new):
    """ Replace part of string with new string

    Beginning at startpos, replace everything up to endpos
    with the new string. Note that new string can be different size.

    Arguments:
        string: Original string
        startpos: Where to begin replace in string. Strings begin at position zero.
        endpos: Where to end replace in string. Strings end at len(string).
        new: New string to replace with

    Returns:
        Returns a new string with the value of new string inserted between startpos and endpos

    Example:
        # Hello awesome replacer
        substr_replace("Hello World", 6, 11, "awesome replacer")
    """
    s_before = string[:startpos]
    s_after = string[endpos:]

    return s_before + new + s_after

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
        self.ascii_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.integers = "0123456789"

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

    def __init__(self, pattern=None, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern

        self.regex = re.compile(r"""
            (?P<character>\\[cd](\{\d\})?)
            | (?P<range>\[[\w]-[\w]\](\{\d\})?)
            | (?P<oneof>\[\w+\](\{\d\})?)
        """, re.VERBOSE)

    def _character(self, fmt):
        """ Generate a single character """
        (character, quantifier) = re.match(r"\\([cd])(?:\{(\d)\})?", fmt).groups()
        if quantifier is None:
            quantifier = 1
        else:
            quantifier = int(quantifier)

        result = ""
        for _ in range(quantifier):
            if character == "c":
                result += self.rnd.choice(self.ascii_characters)
            else:
                result += self.rnd.choice(self.integers)

        return result

    def _range(self, fmt):
        """ Generate a single character from a range """
        (start, end, quantifier) = re.match(r"\[(.)-(.)\](?:\{(\d)\})?", fmt).groups()
        if quantifier is None:
            quantifier = 1
        else:
            quantifier = int(quantifier)

        # Comparing start and end as string characters means
        # the comparison work for both letters and integers
        if start >= end:
            raise ValueError("Inversed range start and end")

        characters = ""
        if re.match(r"\d\d", start+end):
            # Integer range
            characters = slicer(self.integers, start, end)
        elif re.match(r"[a-zA-Z][a-zA-Z]", start+end):
            # Letter range
            characters = slicer(self.ascii_characters, start, end)
        else:
            raise ValueError("Invalid range")

        result = ""
        for _ in range(quantifier):
            result += self.rnd.choice(characters)

        return result

    def _oneof(self, fmt):
        (characters, quantifier) = re.match(r"\[(\w+)\](?:\{(\d)\})?", fmt).groups()
        if quantifier is None:
            quantifier = 1
        else:
            quantifier = int(quantifier)

        result = ""
        for _ in range(quantifier):
            result += self.rnd.choice(characters)

        return result

    def generate(self):
        """ Generate string from pattern """

        # Pattern contains all literals so use it as a base
        string = self.pattern

        match = re.search(self.regex, string)
        while match:
            fmt = match.group()
            group = match.lastgroup

            # We know there is a match and it must be one of
            # these group names
            if group == "character":
                result = self._character(fmt)
            elif group == "range":
                result = self._range(fmt)
            elif group == "oneof":
                result = self._oneof(fmt)

            string = substr_replace(string, match.start(), match.end(), result)
            match = re.search(self.regex, string)

        return string
