from unittest import TestCase

from flask_seeder.parser import Tokenizer

class TestTokenizer(TestCase):

    def setUp(self):
        self.t = Tokenizer()

    def test_tokenize_CHARCODE(self):
        self.t.run(r"\d")

        self.assertEqual(self.t.next().group, "CHARCODE")

    def test_tokenize_ONEOF(self):
        self.t.run("[abc]")

        self.assertEqual(self.t.next().group, "ONEOF")

    def test_tokenize_RANGE(self):
        self.t.run("[0-9]")

        self.assertEqual(self.t.next().group, "RANGE")

    def test_tokenize_QUANTIFIER(self):
        self.t.run("{1}")

        self.assertEqual(self.t.next().group, "QUANTIFIER")

    def test_tokenize_QUANTIFIER_RANGE(self):
        self.t.run("{1,5}")

        self.assertEqual(self.t.next().group, "QUANTIFIER_RANGE")

    def test_tokenize_STRING_GROUP(self):
        self.t.run("(one|two|three)")

        self.assertEqual(self.t.next().group, "STRING_GROUP")

    def test_tokenize_NUMBER(self):
        self.t.run("123")

        self.assertEqual(self.t.next().group, "NUMBER")

    def test_tokenize_STRING(self):
        self.t.run("string")

        self.assertEqual(self.t.next().group, "STRING")

    def test_tokenize_LITERAL(self):
        self.t.run("]#!.")

        self.assertEqual(self.t.next().group, "LITERAL")

    def test_tokenize_combination(self):
        expected = [
            "STRING",
            "RANGE",
            "QUANTIFIER",
            "CHARCODE",
            "STRING_GROUP",
            "QUANTIFIER_RANGE",
            "ONEOF",
            "QUANTIFIER",
            "NUMBER"
        ]

        self.t.run("abc[0-9]{5}\\d(one|two){1,2}[qwerty]{2}123")

        groups = [grp.group for grp in self.t.tokens]

        self.assertListEqual(groups, expected)

    def test_next_return_None_when_no_tokens_remain(self):
        self.assertIsNone(self.t.next())

    def test_peek_return_None_when_no_tokens_remain(self):
        self.assertIsNone(self.t.peek())

    def test_peek_return_next_token_without_moving_cursor(self):
        self.t.run("abc")

        self.assertEqual(self.t.peek(), self.t.peek())
