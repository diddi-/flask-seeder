from unittest import TestCase
from unittest.mock import MagicMock

from flask_seeder.parser import SGParser, Token, strtype


class TestUtility(TestCase):

    def test_strtype_return_DIGIT_type(self):
        result = strtype("123")

        self.assertEqual(result, "DIGIT")

    def test_strtype_return_ALPHA_type(self):
        result = strtype("abc")

        self.assertEqual(result, "ALPHA")

    def test_strtype_return_STRING_type(self):
        result = strtype("abc123#.}")

        self.assertEqual(result, "STRING")

class TestSGParser(TestCase):

    def setUp(self):
        self.tokenizer = MagicMock()
        self.parser = SGParser(tokenizer=self.tokenizer)

    def test_parse_string(self):
        expected = {"type": "STRING", "value": "qwerty"}
        token = Token("STRING", "qwerty")

        result = self.parser.parse_STRING(token)

        self.assertDictEqual(result, expected)

    def test_parse_range(self):
        expected = {"type": "RANGE", "value": {"start": "1", "end": "2"},
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 1,
                    }}
        token = Token("RANGE", "[1-2]")

        result = self.parser.parse_RANGE(token)

        self.assertDictEqual(result, expected)

    def test_parse_range_raise_RuntimeError_for_inversed_range(self):
        token = Token("RANGE", "[2-1]")

        with self.assertRaises(ValueError):
            self.parser.parse_RANGE(token)

    def test_prase_range_raise_RuntimeError_for_mixed_start_end(self):
        token = Token("RANGE", "[1-z]")

        with self.assertRaises(ValueError):
            self.parser.parse_RANGE(token)


    def test_parse_quantifier(self):
        expected = {"type": "QUANTIFIER", "value": 5}
        token = Token("QUANTIFIER", "{5}")

        result = self.parser.parse_QUANTIFIER(token)

        self.assertDictEqual(result, expected)

    def test_parse_range_with_quantifier(self):
        expected = {"type": "RANGE",
                    "value": {
                        "start": "1",
                        "end": "2"
                    },
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 5
                    }}
        range_token = Token("RANGE", "[1-2]")
        quant_token = Token("QUANTIFIER", "{5}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_RANGE(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_range_with_quantifier_range(self):
        expected = {"type": "RANGE",
                    "value": {
                        "start": "1",
                        "end": "2"
                    },
                    "repeat": {
                        "type": "QUANTIFIER_RANGE",
                        "value": {
                            "start": 5,
                            "end": 10
                        }
                    }}
        range_token = Token("RANGE", "[1-2]")
        quant_token = Token("QUANTIFIER_RANGE", "{5,10}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_RANGE(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_charcode(self):
        expected = {"type": "CHARCODE", "value": "d",
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 1,
                    }}
        token = Token("CHARCODE", r"\d")

        result = self.parser.parse_CHARCODE(token)

        self.assertDictEqual(result, expected)

    def test_parse_charcode_with_quantifier(self):
        expected = {"type": "CHARCODE",
                    "value": "d",
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 2}}
        range_token = Token("CHARCODE", r"\d")
        quant_token = Token("QUANTIFIER", "{2}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_CHARCODE(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_charcode_with_quantifier_range(self):
        expected = {"type": "CHARCODE",
                    "value": "d",
                    "repeat": {
                        "type": "QUANTIFIER_RANGE",
                        "value": {
                            "start": 5,
                            "end": 10
                        }
                    }}
        range_token = Token("CHARCODE", r"\d")
        quant_token = Token("QUANTIFIER_RANGE", "{5,10}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_CHARCODE(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_oneof(self):
        expected = {"type": "ONEOF", "value": ["a", "b", "c"],
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 1,
                    }}
        token = Token("ONEOF", "[abc]")

        result = self.parser.parse_ONEOF(token)

        self.assertDictEqual(result, expected)

    def test_parse_oneof_with_quantifier(self):
        expected = {"type": "ONEOF",
                    "value": ["a", "b", "c"],
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 2
                    }}
        range_token = Token("ONEOF", "[abc]")
        quant_token = Token("QUANTIFIER", "{2}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_ONEOF(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_oneof_with_quantifier_range(self):
        expected = {"type": "ONEOF",
                    "value": ["a", "b", "c"],
                    "repeat": {
                        "type": "QUANTIFIER_RANGE",
                        "value": {
                            "start": 5,
                            "end": 10
                        }
                    }}
        range_token = Token("ONEOF", "[abc]")
        quant_token = Token("QUANTIFIER_RANGE", "{5,10}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_ONEOF(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_quantifier_range(self):
        expected = {"type": "QUANTIFIER_RANGE", "value": {"start": 1, "end": 2}}
        token = Token("QUANTIFIER_RANGE", "{1,2}")

        result = self.parser.parse_QUANTIFIER_RANGE(token)

        self.assertDictEqual(result, expected)

    def test_parse_quantifier_range_raise_RuntimeError_for_inversed_range(self):
        token = Token("QUANTIFIER_RANGE", "{2,1}")

        with self.assertRaises(ValueError):
            self.parser.parse_QUANTIFIER_RANGE(token)

    def test_parse_string_group(self):
        expected = {"type": "STRING_GROUP", "value": ["one", "two", "three"],
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 1,
                    }}
        token = Token("STRING_GROUP", "(one|two|three)")

        result = self.parser.parse_STRING_GROUP(token)

        self.assertDictEqual(result, expected)

    def test_parse_string_group_with_quantifier(self):
        expected = {"type": "STRING_GROUP",
                    "value": ["one", "two"],
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 3
                    }}
        range_token = Token("STRING_GROUP", "(one|two)")
        quant_token = Token("QUANTIFIER", "{3}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_STRING_GROUP(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_string_group_with_quantifier_range(self):
        expected = {"type": "STRING_GROUP",
                    "value": ["one", "two"],
                    "repeat": {
                        "type": "QUANTIFIER_RANGE",
                        "value": {
                            "start": 5,
                            "end": 10
                        }
                    }}
        range_token = Token("STRING_GROUP", "(one|two)")
        quant_token = Token("QUANTIFIER_RANGE", "{5,10}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_STRING_GROUP(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_number(self):
        expected = {"type": "NUMBER", "value": 123,
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 1,
                    }}
        token = Token("NUMBER", "123")

        result = self.parser.parse_NUMBER(token)

        self.assertDictEqual(result, expected)

    def test_parse_number_with_quantifier(self):
        expected = {"type": "NUMBER",
                    "value": 123,
                    "repeat": {
                        "type": "QUANTIFIER",
                        "value": 3
                    }}
        range_token = Token("NUMBER", "123")
        quant_token = Token("QUANTIFIER", "{3}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_NUMBER(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_number_with_quantifier_range(self):
        expected = {"type": "NUMBER",
                    "value": 123,
                    "repeat": {
                        "type": "QUANTIFIER_RANGE",
                        "value": {
                            "start": 5,
                            "end": 10
                        }
                    }}
        range_token = Token("NUMBER", "123")
        quant_token = Token("QUANTIFIER_RANGE", "{5,10}")
        self.tokenizer.peek.return_value = quant_token
        self.tokenizer.next.return_value = quant_token

        result = self.parser.parse_NUMBER(range_token)

        self.assertDictEqual(result, expected)

    def test_parse_literal(self):
        expected = {"type": "LITERAL", "value": "#(]"}
        token = Token("LITERAL", "#(]")

        result = self.parser.parse_LITERAL(token)

        self.assertDictEqual(result, expected)
