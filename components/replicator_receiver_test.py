import unittest

from components.replicator_receiver import ReplicatorReceiver
from constants.codes import Code
from constants.datasets import Dataset


class ReplicatorReceiverTest(unittest.TestCase):
    def test_map_code_to_dataset_valid_1(self):
        self.assertEqual(Dataset.Dataset_1, ReplicatorReceiver.map_code_to_dataset(Code.CODE_DIGITAL))

    def test_map_code_to_dataset_valid_2(self):
        self.assertEqual(Dataset.Dataset_2, ReplicatorReceiver.map_code_to_dataset(Code.CODE_CUSTOM))

    def test_map_code_to_dataset_valid_3(self):
        self.assertEqual(Dataset.Dataset_3, ReplicatorReceiver.map_code_to_dataset(Code.CODE_SINGLENOE))

    def test_map_code_to_dataset_valid_4(self):
        self.assertEqual(Dataset.Dataset_4, ReplicatorReceiver.map_code_to_dataset(Code.CODE_SOURCE))

    def test_map_code_to_dataset_invalid(self):
        self.assertEqual(None, ReplicatorReceiver.map_code_to_dataset(''))

    def test_map_dataset_to_dataset_id_valid_1(self):
        self.assertEqual(1, ReplicatorReceiver.map_dataset_to_dataset_id(Dataset.Dataset_1))

    def test_map_dataset_to_dataset_id_valid_2(self):
        self.assertEqual(2, ReplicatorReceiver.map_dataset_to_dataset_id(Dataset.Dataset_2))

    def test_map_dataset_to_dataset_id_valid_3(self):
        self.assertEqual(3, ReplicatorReceiver.map_dataset_to_dataset_id(Dataset.Dataset_3))

    def test_map_dataset_to_dataset_id_valid_4(self):
        self.assertEqual(4, ReplicatorReceiver.map_dataset_to_dataset_id(Dataset.Dataset_4))

    def test_map_dataset_to_dataset_id_invalid(self):
        self.assertEqual(None, ReplicatorReceiver.map_dataset_to_dataset_id(''))


if __name__ == '__main__':
    unittest.main()
