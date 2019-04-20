from unittest import TestCase
from unittest.mock import MagicMock

from flask_seeder.generator import Integer

class TestIntegerGenerator(TestCase):

    def setUp(self):
        self.rnd_mock = MagicMock()
        self.generator = Integer(rnd=self.rnd_mock)

    def test_generate_int_with_default_values(self):
        self.generator.generate()

        self.rnd_mock.randint.assert_called_once_with(
            self.generator.start,
            self.generator.end
        )

    def test_generate_int_with_custom_values(self):
        self.generator.start = 10
        self.generator.end = 20

        self.generator.generate()
        self.rnd_mock.randint.assert_called_once_with(
            self.generator.start,
            self.generator.end
        )