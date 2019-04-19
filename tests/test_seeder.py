from unittest import TestCase
from flask_seeder import Seeder

class TestBaseSeeder(TestCase):

    def setUp(self):
        self.seeder = Seeder()

    def test_run_raise_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            self.seeder.run()

