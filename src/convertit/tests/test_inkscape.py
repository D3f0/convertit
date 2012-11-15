import os
import shutil
import unittest
import filecmp

from mock import patch

from convertit.converters import inkscape


here = os.path.dirname(os.path.realpath(__file__))


class InkscapeRegisterTests(unittest.TestCase):
    @patch('convertit.converters.inkscape.exists')
    def test_registered_when_inkscape_exists(self, exists_mock):
        exists_mock.return_value = True
        converters = {}
        inkscape.register(converters)
        self.assertIn('image/svg+xml', converters)

    @patch('convertit.converters.inkscape.exists')
    def test_not_registered_when_inkscape_not_exists(self, exists_mock):
        exists_mock.return_value = False
        converters = {}
        inkscape.register(converters)
        self.assertNotIn('image/svg+xml', converters)


class InkscapeConvertionTests(unittest.TestCase):
    temp_dir = os.path.join(here, 'data/tmp')
    document_filepath = os.path.join(here, 'data/test_svg.svg')
    reference_filepath = os.path.join(here, 'data/test_svg.pdf')

    def setUp(self):
        if not inkscape.exists():
            self.skipTest('inkscape not found')

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        os.makedirs(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_svg_conversion(self):
        converted_filepath = os.path.join(self.temp_dir, 'test_svg.pdf')
        inkscape.to_pdf(self.document_filepath, converted_filepath)
        self.assertTrue(os.path.exists(converted_filepath))
