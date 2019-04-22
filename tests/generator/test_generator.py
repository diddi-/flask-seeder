from unittest import TestCase
from unittest.mock import MagicMock, patch, mock_open

from flask_seeder.generator import Generator, resource_path, read_resource, slicer

MOCK_CONTENTS = "line1\nline2"

class TestGenerator(TestCase):

    def setUp(self):
        self.rnd_mock = MagicMock()
        self.generator = Generator(rnd=self.rnd_mock)


    def test_generate_raise_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            self.generator.generate()

    @patch("flask_seeder.generator.pkg_resources")
    def test_resource_path(self, m_pkg):
        resource_path("test")

        m_pkg.resource_filename.assert_called_once()

    @patch("flask_seeder.generator.resource_path", return_value="test")
    @patch("flask_seeder.generator.open", mock_open(read_data=MOCK_CONTENTS))
    def test_read_resource_return_contents_as_list(self, m_open):
        expected = [
            "line1",
            "line2"
        ]

        result = read_resource("test")

        self.assertListEqual(result, expected)

    def test_slicer_return_new_string(self):
        original = "abcdefghijklmnopqrstuvwxyz"
        expected = "ijklmno"

        result = slicer(original, "i", "o")

        self.assertEqual(result, expected)

    def test_slicer_return_None_if_no_slice_is_found(self):
        original = "abcdefghijklmnopqrstuvwxyz"

        # Inversed start/end
        result = slicer(original, "z", "a")

        self.assertIsNone(result)
