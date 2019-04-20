from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from flask_seeder.generator import Name

MOCK_CONTENTS = [
    "name1",
    "name2"
]

class TestNameGenerator(TestCase):

    def setUp(self):
        self.rnd_mock = MagicMock()
        self.generator = Name(rnd=self.rnd_mock)

    @patch("flask_seeder.generator.read_resource", return_value=MOCK_CONTENTS)
    def test_generate_name(self, m_read_resource):
        result = self.generator.generate()

        self.rnd_mock.choice.assert_called_once_with(MOCK_CONTENTS)
