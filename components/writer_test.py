import unittest
from unittest.mock import patch

from components.writer import Writer


class WriterTest(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    def test_ask_for_input_valid(self, p):
        Writer.is_running = True
        self.assertEqual(1, Writer.ask_for_input(1))


if __name__ == '__main__':
    unittest.main()
