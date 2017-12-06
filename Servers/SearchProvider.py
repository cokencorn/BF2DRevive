import socket
from threading import Thread
from Models.AccountConnection import AccountConnection


class SearchProvider(Thread):
    type = "SP"

    def __init__(self, host, port, db):
        super(SearchProvider, self).__init__()
        self.host = host
        self.port = port
        self.db = db
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def run(self):
        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            # print "SP: Accepted connection from a client"
            conn = AccountConnection(self, address, client, self.db)
            conn.start()
