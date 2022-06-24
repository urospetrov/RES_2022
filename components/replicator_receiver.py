import pickle
import socket
import time
from _thread import start_new_thread
from os import getcwd
from random import randint
from sys import path

from config import PORT_REPLICATOR_RECEIVER, REPLICATOR_RECEIVER_FORWARDING_TIMER, DELTA_CD_CAP
from constants.codes import Code
from constants.datasets import Dataset
from constants.readers import readers
from logger import Logger
from models.collection_description import CollectionDescription
from models.delta_cd import DeltaCD
from models.historical_collection import HistoricalCollection
from models.receiver_property import ReceiverProperty

path.append(getcwd()[1:-11])


class ReplicatorReceiver:
    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer: list[CollectionDescription] = [
        CollectionDescription(1, Dataset.Dataset_1, HistoricalCollection([])),
        CollectionDescription(2, Dataset.Dataset_2, HistoricalCollection([])),
        CollectionDescription(3, Dataset.Dataset_3, HistoricalCollection([])),
        CollectionDescription(4, Dataset.Dataset_4, HistoricalCollection([])),
    ]
    cd_structure: DeltaCD = DeltaCD([], [])
    is_running: bool = False

    @staticmethod
    def start():  # pragma: no cover
        ReplicatorReceiver.is_running = True
        ReplicatorReceiver.start_server()
        start_new_thread(ReplicatorReceiver.accept_connections, ())
        start_new_thread(ReplicatorReceiver.forward_data, ())
        ReplicatorReceiver.close()

    @staticmethod
    def start_server():  # pragma: no cover
        ReplicatorReceiver.server_socket = socket.socket()
        try:
            ReplicatorReceiver.server_socket.bind((socket.gethostname(), PORT_REPLICATOR_RECEIVER))
        except socket.error:
            ReplicatorReceiver.is_running = False
            exit()
        ReplicatorReceiver.server_socket.listen()

    @staticmethod
    def accept_connections():  # pragma: no cover
        client_socket, _ = ReplicatorReceiver.server_socket.accept()
        print('Replicator sender connected')
        ReplicatorReceiver.receiver_messages(client_socket)

    @staticmethod
    def receiver_messages(client_socket: socket.socket):  # pragma: no cover
        while ReplicatorReceiver.is_running:
            try:
                msg = client_socket.recv(2048)
                msg = pickle.loads(msg)
                msg_type = msg[0]
                msg_data = msg[1]
                if msg_type == 'ITEM':
                    ReplicatorReceiver.save_data(msg_data)
                    Logger.log_action(f'[REPLICATOR RECEIVER]: Received item: {msg_data}')
                    print(f'Received item: {msg_data}')
            except:
                continue

    @staticmethod
    def save_data(receiver_property: ReceiverProperty):  # pragma: no cover
        dataset = ReplicatorReceiver.map_code_to_dataset(receiver_property.code)
        index = 0
        for cd in ReplicatorReceiver.buffer:
            if cd.dataset != dataset:
                index += 1
                continue

            ReplicatorReceiver.buffer[index].historical_collection.receiver_properties.append(receiver_property)

    @staticmethod
    def forward_data():  # pragma: no cover
        while ReplicatorReceiver.is_running:
            time.sleep(REPLICATOR_RECEIVER_FORWARDING_TIMER)
            for cd in ReplicatorReceiver.buffer:
                if len(cd.historical_collection.receiver_properties) == 0:
                    continue

                _ = randint(0, 1)
                if _ == 1:
                    ReplicatorReceiver.cd_structure.add.append(cd)
                else:
                    ReplicatorReceiver.cd_structure.update.append(cd)

                if len(ReplicatorReceiver.cd_structure.add) + len(
                        ReplicatorReceiver.cd_structure.update) < DELTA_CD_CAP:
                    continue

                ReplicatorReceiver.cd_structure.add.clear()
                ReplicatorReceiver.cd_structure.update.clear()

                reader_id = ReplicatorReceiver.map_dataset_to_dataset_id(cd.dataset)
                reader = readers[reader_id]
                reader.save_data(cd)
                Logger.log_action(f'[INFO]: Sending data to {reader}')
                print(f'[INFO]: Sending data to {reader}')
                cd.historical_collection.receiver_properties.clear()

    # Tested
    @staticmethod
    def map_code_to_dataset(code: Code):
        if code in Dataset.Dataset_1.value:
            return Dataset.Dataset_1
        elif code in Dataset.Dataset_2.value:
            return Dataset.Dataset_2
        elif code in Dataset.Dataset_3.value:
            return Dataset.Dataset_3
        elif code in Dataset.Dataset_4.value:
            return Dataset.Dataset_4

    # Tested
    @staticmethod
    def map_dataset_to_dataset_id(dataset: Dataset):
        if dataset == Dataset.Dataset_1:
            return 1
        elif dataset == Dataset.Dataset_2:
            return 2
        elif dataset == Dataset.Dataset_3:
            return 3
        elif dataset == Dataset.Dataset_4:
            return 4

    @staticmethod
    def close():  # pragma: no cover
        print('Press enter to close')
        input()
        ReplicatorReceiver.is_running = False
        exit()


if __name__ == '__main__':  # pragma: no cover
    ReplicatorReceiver.start()
