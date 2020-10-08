import uuid

from unittest import TestCase
from unittest.mock import MagicMock, patch

from flask_seeder.generator import UUID


class TestUUIDGenerator(TestCase):
    def setUp(self):
        self.generator = UUID()

    @patch("uuid.uuid4", return_value=0)
    def test_generate_mock_uuid(self, m_uuid):
        result = self.generator.generate()

        assert result == 0

    def test_generate_uuid(self):
        result = self.generator.generate()
        
        self.assertEqual(4, uuid.UUID(str(result), version=4).version)
