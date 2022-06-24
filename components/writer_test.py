import unittest
from unittest.mock import patch

from components.writer import Writer


class WriterTest(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    def test_ask_for_input_valid(self, p):
        Writer.is_running = True
        self.assertEqual(1, Writer.ask_for_input(1))

    @patch('builtins.input', return_value='2022-12-22')
    def test_get_date(self, p):
        self.assertEqual('2022-12-22', Writer.get_date(''))

    @patch('builtins.input', return_value='11:11:11')
    def test_get_time(self, p):
        self.assertEqual('11:11:11', Writer.get_time(''))


if __name__ == '__main__':
    unittest.main()
