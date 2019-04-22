""" String Generator pattern parser """

import re

# pylint: disable=bad-whitespace
TOKEN_MATCHERS = [
    ("CHARCODE",            r"\\([a-z])"),
    ("ONEOF",               r"\[([a-zA-Z0-9]+)\]"),
    ("RANGE",               r"\[(\w)-(\w)\]"),
    ("QUANTIFIER",          r"\{(\d+)\}"),
    ("QUANTIFIER_RANGE",    r"\{(\d*),(\d+)\}"),
    ("STRING_GROUP",        r"\(([^|]([^)]+))\)"),
    ("NUMBER",              r"\d+"),
    ("STRING",              r"[a-zA-Z]+"),
    ("LITERAL",             r"."),
]

def strtype(string):
    """ Check string type

    Arguments:
        string: String to check

    Returns:
        Returns one of the following results
        * DIGIT: String is digit [0-9]
        * ALPHA: String is alpha [a-zA-Z]
        * STRING: If no other match is found, it is assumed to be a STRING type
    """
    if str.isdigit(string):
        return "DIGIT"
    if str.isalpha(string):
        return "ALPHA"
    return "STRING"

class Token: # pylint: disable=too-few-public-methods
    """ Token class
    Used by a tokenizer to store token data

    Attributes:
        group: Token group type or classification
        value: Token value
        pos: Starting position in input stream where token is found
    """

    def __init__(self, group, value, pos=0):
        self.group = group
        self.value = value
        self.pos = pos


class Tokenizer:
    """ String Generator Tokenizer

    Attributes:
        string: String to tokenize
        tokens: List of tokens after successful tokenization
    """

    def __init__(self):
        self.tokens = []
        self.regex = "|".join("(?P<%s>%s)" % matcher for matcher in TOKEN_MATCHERS)
        self._cursor = 0

    def run(self, string=None):
        """ Run tokenizer """
        for match in re.finditer(self.regex, string):
            group = match.lastgroup
            value = match.group()
            self.tokens.append(Token(group, value, match.start()))

    def next(self):
        """ Get next token

        Retrieve next token and move cursor forward.

        Returns:
            A Token instance
        """
        if self._cursor >= len(self.tokens):
            return None

        token = self.tokens[self._cursor]
        self._cursor += 1
        return token

    def peek(self):
        """ Peek at the next token

        Retrieve next token without moving cursor forward.

        Returns:
            A Token instance
        """
        if self._cursor >= len(self.tokens):
            return None

        return self.tokens[self._cursor]

class SGParser:
    """ String Generator Pattern parser """

    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer

    def _repeat(self):
        ahead = self.tokenizer.peek()
        if ahead and ahead.group == "QUANTIFIER":
            result = self.parse_QUANTIFIER(self.tokenizer.next())
        elif ahead and ahead.group == "QUANTIFIER_RANGE":
            result = self.parse_QUANTIFIER_RANGE(self.tokenizer.next())
        else:
            result = {"type": "QUANTIFIER", "value": 1}

        return result

    def parse_STRING(self, token): # pylint: disable=invalid-name, no-self-use
        """ Parse a STRING token

        Returns:
            Dictionary representing the AST node structure for string
        """
        return {"type": token.group, "value": token.value}

    def parse_RANGE(self, token): # pylint: disable=invalid-name
        """ Parse a RANGE token

        Returns:
            Dictionary representing the AST node structure for range
        """
        (start, end) = re.search(r"\[([a-zA-Z0-9])-([a-zA-Z0-9])\]", token.value).groups()
        if start > end or strtype(start) != strtype(end):
            raise ValueError("Invalid range %s at position %d" % (token.value, token.pos))

        result = {"type": token.group,
                  "value": {
                      "start": start,
                      "end": end,
                  },
                  "repeat": self._repeat()}

        return result

    def parse_QUANTIFIER(self, token): # pylint: disable=invalid-name, no-self-use
        """ Parse a QUANTIFIER token

        Returns:
            Dictionary representing the AST node structure for quantifier
        """
        value = re.match(r"\{(\d+)\}", token.value).group(1)
        return {"type": token.group, "value": int(value)}

    def parse_CHARCODE(self, token): # pylint: disable=invalid-name
        """ Parse a CHARCODE token

        Returns:
            Dictionary representing the AST node structure for charcode
        """
        value = re.match(r"\\([a-z])", token.value).group(1)
        return {"type": token.group, "value": value, "repeat": self._repeat()}

    def parse_ONEOF(self, token): # pylint: disable=invalid-name
        """ Parse a ONEOF token

        Returns:
            Dictionary representing the AST node structure for oneof
        """
        values = re.findall("[a-zA-Z0-9]", token.value)
        return {"type": token.group, "value": values, "repeat": self._repeat()}

    def parse_QUANTIFIER_RANGE(self, token): # pylint: disable=invalid-name, no-self-use
        """ Parse a QUANTIFIER_RANGE token

        Returns:
            Dictionary representing the AST node structure for quantifier range
        """
        (start, end) = re.search(r"\{(\d+),(\d+)\}", token.value).groups()

        if int(start) > int(end):
            raise ValueError("Invalid range %s at %d" % (token.value, token.pos))

        return {"type": token.group, "value": {"start": int(start), "end": int(end)}}

    def parse_STRING_GROUP(self, token): # pylint: disable=invalid-name
        """ Parse a STRING_GROUP token

        Returns:
            Dictionary representing the AST node structure for string group
        """
        options = re.match(r"\((.+)\)", token.value).group(1)
        values = re.split(r"\|", options)
        return {"type": token.group, "value": values, "repeat": self._repeat()}

    def parse_NUMBER(self, token): # pylint: disable=invalid-name
        """ Parse a NUMBER token

        Returns:
            Dictionary representing the AST node structure for number
        """
        return {"type": token.group, "value": int(token.value), "repeat": self._repeat()}

    def parse_LITERAL(self, token): # pylint: disable=invalid-name, no-self-use
        """ Parse a LITERAL token

        Returns:
            Dictionary representing the AST node structure for literal
        """
        return {"type": "LITERAL", "value": token.value}

    def parse(self, string):
        """ Main parser method

        Parses a list of tokens into an AST

        Arguments:
            string: The string to be parsed

        Returns:
            Dictionary representing the String Generator pattern AST
        """
        ast = []
        self.tokenizer.run(string)
        token = self.tokenizer.next()
        while token:
            function_name = "parse_" + token.group
            if not hasattr(self, function_name):
                function_name = "parse_LITERAL"

            func = getattr(self, function_name)
            ast.append(func(token))

            token = self.tokenizer.next()

        return ast
