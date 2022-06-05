import socket
import threading
import pickle
from collections import deque


class TestClass:

    def __init__(self, id):
        self.id = id


HEADER = 4096
PORT = 5052
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

red = deque()

print(SERVER + ":" + str(PORT))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    data = conn.recv(HEADER)
    data_variable = pickle.loads(data)
    print(data_variable.id)
    red.append(data_variable)
    print(red.popleft().id)
    print("Data recieved from client")
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