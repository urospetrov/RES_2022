import socket
import threading
import pickle
from collections import deque


class TestClass:

    def __init__(self, id):
        self.id = id


HEADER = 4096
PORT = 5050
PORT2 = 5051
SERVER = socket.gethostbyname(socket.gethostname())
SERVER2 = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
ADDR2 = (SERVER2, PORT2)

red = deque()

print(SERVER + ":" + str(PORT))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.connect(ADDR2)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    data = conn.recv(HEADER)
    data_variable = pickle.loads(data)
    print(data_variable.id)
    red.append(data_variable)
    print("Data recieved from client")

    data_string = pickle.dumps(red.popleft())
    sender.send(data_string)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] Server is starting...")
start()