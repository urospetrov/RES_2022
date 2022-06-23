import pickle
import socket
import time
from _thread import start_new_thread
from os import getcwd
from sys import path

from config import PORT_REPLICATOR_SENDER, PORT_REPLICATOR_RECEIVER, REPLICATOR_SENDER_TIMER
from logger import Logger
from models.receiver_property import ReceiverProperty
from utils.connection import Connection

path.append(getcwd()[1:-11])


class ReplicatorSender:
    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    replicator_receiver_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer: list[ReceiverProperty] = []
    is_connected: bool = False
    is_running: bool = False

    @staticmethod
    def start():  # pragma: no cover
        ReplicatorSender.is_running = True
        ReplicatorSender.start_server()
        start_new_thread(ReplicatorSender.accept_connections, ())
        start_new_thread(ReplicatorSender.connect, ())
        start_new_thread(ReplicatorSender.forward_data, ())
        ReplicatorSender.close()

    @staticmethod
    def connect():  # pragma: no cover
        ReplicatorSender.replicator_receiver_socket = Connection.connect(PORT_REPLICATOR_RECEIVER)
        Logger.log_action('[INFO]: Forwarding data to replicator receiver')
        print('[INFO]: Forwarding data')
        ReplicatorSender.is_connected = True

    @staticmethod
    def reconnect():  # pragma: no cover
        Logger.log_action('[INFO]: ReplicatorSender reconnecting')
        print('[INFO]: Reconnecting')
        ReplicatorSender.is_connected = False
        ReplicatorSender.connect()

    @staticmethod
    def start_server():  # pragma: no cover
        ReplicatorSender.server_socket = socket.socket()
        try:
            ReplicatorSender.server_socket.bind((socket.gethostname(), PORT_REPLICATOR_SENDER))
        except socket.error:
            ReplicatorSender.is_running = False
            exit()
        ReplicatorSender.server_socket.listen()

    @staticmethod
    def accept_connections():  # pragma: no cover
        while ReplicatorSender.is_running:
            client_socket, _ = ReplicatorSender.server_socket.accept()
            print('Client connected')
            start_new_thread(ReplicatorSender.receiver_messages, (client_socket,))

    @staticmethod
    def receiver_messages(client_socket: socket.socket):  # pragma: no cover
        while ReplicatorSender.is_running:
            try:
                msg = client_socket.recv(2048)
                msg = pickle.loads(msg)
                msg_type = msg[0]
                msg_data = msg[1]
                if msg_type == 'ITEM':
                    ReplicatorSender.buffer.append(msg_data)
                    Logger.log_action(f'[REPLICATOR SENDER]: Received item: {msg_data}')
                    print(f'Received item: {msg_data}')
            except:
                continue

    @staticmethod
    def forward_data():  # pragma: no cover
        while ReplicatorSender.is_running:
            if ReplicatorSender.is_connected:
                time.sleep(REPLICATOR_SENDER_TIMER)
                for item in ReplicatorSender.buffer:
                    package = ('ITEM', item)
                    package = pickle.dumps(package)
                    try:
                        ReplicatorSender.replicator_receiver_socket.send(package)
                        ReplicatorSender.buffer.remove(item)
                    except socket.error:
                        ReplicatorSender.reconnect()

    @staticmethod
    def close():  # pragma: no cover
        print('Press enter to close')
        input()
        ReplicatorSender.is_running = False
        exit()


if __name__ == '__main__':
    ReplicatorSender.start()
