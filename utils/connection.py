import pickle
import socket


class Connection:
    @staticmethod
    def connect(port: int):  # pragma: no cover
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                client_socket.connect((socket.gethostname(), port))
                return client_socket
            except:
                continue

    @staticmethod
    def send_message(client_socket, message):  # pragma: no cover
        package = pickle.dumps(message)
        try:
            client_socket.send(package)
            return True
        except:
            return False
