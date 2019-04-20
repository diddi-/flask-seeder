from unittest import TestCase
from unittest.mock import MagicMock

from flask_seeder.generator import Sequence

class TestSequenceGenerator(TestCase):

    def setUp(self):
        self.rnd_mock = MagicMock()
        self.generator = Sequence(rnd=self.rnd_mock)


    def test_generate_sequential_numbers(self):
        first = self.generator.generate()
        second = self.generator.generate()

        self.assertTrue(first+1 == second)

    def test_generate_sequential_start_end(self):
        self.generator.start = 23
        self.generator.end = 25

        first = self.generator.generate()
        second = self.generator.generate()

        self.assertEqual(first, 23)
        self.assertEqual(second, 24)

    def test_generate_raise_RuntimeError_when_exhausted(self):
        # Make start larger than end to trigger RuntimeError
        self.generator.start = 10
        self.generator.end = 5

        with self.assertRaises(RuntimeError):
            self.generator.generate()