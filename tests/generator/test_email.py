from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch, call

from flask_seeder.generator import Email

MOCK_DOMAINS = [
    "domain1.com",
]

MOCK_NAMES = [
    "test1",
]


def read_resource(arg):
    if arg == "domains/domains.txt":
        return MOCK_DOMAINS

    if arg == "names/names.txt":
        return MOCK_NAMES


class TestEmailGenerator(TestCase):
    def setUp(self):
        self.rnd_mock = MagicMock(
            choice=MagicMock(side_effect=lambda values: values[0])
        )
        self.generator = Email(rnd=self.rnd_mock)

    @patch("flask_seeder.generator.read_resource", side_effect=read_resource)
    def test_generate_email(self, m_read_resource):
        result = self.generator.generate()

        self.rnd_mock.choice.assert_has_calls(
            [call(MOCK_NAMES), call(MOCK_DOMAINS)], any_order=True
        )

        assert result == f"{MOCK_NAMES[0]}@{MOCK_DOMAINS[0]}"
