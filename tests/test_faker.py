from unittest import TestCase

from flask_seeder import Faker
from flask_seeder.generator import Generator

class Dummy:
    def __init__(self, test_arg=None):
        self.test_arg = test_arg

class TestFaker(TestCase):

    def setUp(self):
        self.faker = Faker(cls=Dummy)

    def test_create_return_instance(self):
        result = self.faker.create()

        self.assertIsInstance(result[0], Dummy)

    def test_create_with_limit(self):
        result = self.faker.create(2)

        self.assertEqual(len(result), 2)

    def test_create_instantiate_with_init_args_value(self):
        self.faker.init = {"test_arg": "test_value"}

        result = self.faker.create()

        self.assertEqual(result[0].test_arg, "test_value")

    def test_create_run_init_args_generator(self):
        class DummyGenerator(Generator):
            def generate(self):
                return "test_value"
        self.faker.init = {"test_arg": DummyGenerator()}

        result = self.faker.create()

        self.assertEqual(result[0].test_arg, "test_value")
