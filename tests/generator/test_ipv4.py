from ipaddress import IPv4Address

from unittest import TestCase
from unittest.mock import MagicMock, patch

from flask_seeder.generator import IPv4


class TestIPv4Generator(TestCase):
    def setUp(self):
        self.rnd_mock = MagicMock()
        # return value that will be used inside _string_from_ip_int function
        self.rnd_mock.randint.side_effect = [IPv4Address._ALL_ONES]
    

    def test_generate_mock_ipv4_with_default_values(self):
        self.generator = IPv4(rnd=self.rnd_mock)
        self.generator.generate()
        self.rnd_mock.randint.assert_called_once_with(
            0,
            IPv4Address._ALL_ONES
        )
    
    def test_generate_mock_ipv4_returns_a_string(self):
        self.generator = IPv4()
        result = self.generator.generate()
        self.assertEqual(type(result), str)
