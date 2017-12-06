import socket
from threading import Thread
from random import randint
from Models.AccountConnection import AccountConnection


class ClientManager(Thread):
    session_list = []
    type = "CM"

    def __init__(self, host, port, db):
        super(ClientManager, self).__init__()
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
            # print self.session_list
            client, address = self.sock.accept()
            # print "CM: Accepted connection from a client"
            conn = AccountConnection(self, address, client, self.db)
            conn.start()

    def client_disconnect(self, connection):
        if int(connection.session) in self.session_list:
            self.session_list.remove(int(connection.session))

    def generate_session(self):
        # Not the best way. It just works
        session = randint(1000000, 9999999)
        if session not in self.session_list:
            self.session_list.append(session)
            return session
        else:
            return self.generate_session()
