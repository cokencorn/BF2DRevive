import socket
from threading import Thread
from Models.ServerListConnection import ServerListConnection


class ServerListProvider(Thread):
    registered_servers = {}

    def __init__(self, host, port, db):
        super(ServerListProvider, self).__init__()
        self.host = host
        self.port = port
        self.db = db
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 6192)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def run(self):
        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            # print("SP: Accepted connection from a game client")
            conn = ServerListConnection(self, address, client, self.db)
            conn.start()
            conn.join()
