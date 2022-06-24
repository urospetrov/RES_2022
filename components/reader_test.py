import unittest
from unittest.mock import Mock, MagicMock, patch

from components.reader import Reader
from constants.codes import Code
from models.receiver_property import ReceiverProperty

conn = Mock()
curr = Mock()
conn.cursor = MagicMock(return_value=curr)
curr.execute = MagicMock(return_value=None)
curr.fetchone = MagicMock(return_value=None)
conn.close = MagicMock(return_value=None)
curr.close = MagicMock(return_value=None)

r = Reader(1)


class ReaderTest(unittest.TestCase):
    @patch('sqlite3.connect', return_value=conn)
    def test_get_last_value_by_code(self, p):
        self.assertEqual(None, r.get_last_value_by_code(Code.CODE_DIGITAL))

    @patch('sqlite3.connect', return_value=conn)
    def test_save_value(self, p):
        self.assertEqual(None, r.save_value(ReceiverProperty(Code.CODE_DIGITAL, 1)))

    @patch('sqlite3.connect', return_value=conn)
    def test_get_values_by_code(self, p):
        self.assertEqual(None, r.get_values_by_code(Code.CODE_DIGITAL))

    @patch('sqlite3.connect', return_value=conn)
    def test_get_values_by_interval(self, p):
        self.assertEqual(None, r.get_values_by_interval(Code.CODE_DIGITAL, '', '', '', ''))

    def test_map_code_to_dataset_id_valid_1(self):
        self.assertEqual(1, r.map_code_to_dataset_id(Code.CODE_DIGITAL))

    def test_map_code_to_dataset_id_valid_2(self):
        self.assertEqual(2, r.map_code_to_dataset_id(Code.CODE_CUSTOM))

    def test_map_code_to_dataset_id_valid_3(self):
        self.assertEqual(3, r.map_code_to_dataset_id(Code.CODE_SINGLENOE))

    def test_map_code_to_dataset_id_valid_4(self):
        self.assertEqual(4, r.map_code_to_dataset_id(Code.CODE_SOURCE))


if __name__ == '__main__':
    unittest.main()
