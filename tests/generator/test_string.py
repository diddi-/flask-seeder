from unittest import TestCase
from unittest.mock import MagicMock, patch

from flask_seeder.generator import String

class TestStringGenerator(TestCase):

    def setUp(self):
        self.generator = String()

    def test_integer_range_produce_character_from_valid_range(self):
        m_rnd = MagicMock()
        self.generator.rnd = m_rnd
        self.generator.pattern = "[4-6]"

        self.generator.generate()

        m_rnd.choice.assert_called_once_with("456")

    def test_string_range_produce_character_from_valid_range(self):
        m_rnd = MagicMock()
        self.generator.rnd = m_rnd
        self.generator.pattern = "[i-o]"

        self.generator.generate()

        m_rnd.choice.assert_called_once_with("ijklmno")

    def test_integer_range_pattern(self):
        self.generator.pattern = "[0-9]"

        string = self.generator.generate()

        self.assertRegex(string, r"^\d$")

    def test_string_range_pattern(self):
        self.generator.pattern = "[a-z]"

        string = self.generator.generate()

        self.assertRegex(string, "^[a-z]$")

    def test_range_pattern_quantifier(self):
        self.generator.pattern = "[0-9]{5}"

        string = self.generator.generate()

        self.assertRegex(string, r"^\d{5}$")

    def test_multiple_range_patterns(self):
        self.generator.pattern = "[0-9][a-c]"

        string = self.generator.generate()

        self.assertRegex(string, r"^\d[a-c]$")

    def test_multiple_range_patterns_with_quantifiers(self):
        self.generator.pattern = "[0-9]{4}[x-z]{2}"

        string = self.generator.generate()

        self.assertRegex(string, r"^\d{4}[x-z]{2}$")


    def test_integer_character_code(self):
        self.generator.pattern = r"\d"

        string = self.generator.generate()

        self.assertRegex(string, r"^\d$")

    def test_string_character_code(self):
        self.generator.pattern = r"\c"

        string = self.generator.generate()

        self.assertRegex(string, "^[a-zA-Z]$")

    def test_character_code_with_quantifier(self):
        self.generator.pattern = r"\d{3}"

        string = self.generator.generate()

        self.assertRegex(string, r"^\d{3}$")

    def test_oneof_pattern(self):
        self.generator.pattern = r"[aoueiy]"

        string = self.generator.generate()

        self.assertRegex(string, "^[aoueiy]$")

    def test_oneof_pattern_with_quantifier(self):
        self.generator.pattern = r"[aoueiy]{3}"

        string = self.generator.generate()

        self.assertRegex(string, "^[aoueiy]{3}$")

    def test_complex_string_generation(self):
        self.generator.pattern = r"abc\d{4}[i-m]{2}[qwerty]xyz"

        string = self.generator.generate()

        self.assertRegex(string, r"^abc\d{4}[i-m]{2}[qwerty]xyz$")

    def test_charcode_with_quantifier_range(self):
        self.generator.pattern = r"\c{1,2}"

        string = self.generator.generate()

        self.assertRegex(string, "[a-zA-Z]{1,2}")

    def test_invalid_charcode_raise_ValueError(self):
        self.generator.pattern = r"\q"

        with self.assertRaises(ValueError):
            self.generator.generate()

    def test_string_group(self):
        self.generator.pattern = r"(one|two)"

        string = self.generator.generate()

        self.assertRegex(string, r"(one|two)")

    def test_number(self):
        self.generator.pattern = r"123"

        string = self.generator.generate()

        self.assertEqual(string, "123")
