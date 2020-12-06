import socket
import threading
from threading import Thread
from Models.GameServer import GameServer


class ServerListRegister(Thread):
    BF2_AVAILABLE_REQ = bytearray([0x09, 0x00, 0x00, 0x00, 0x00, 0x62, 0x61, 0x74,
                                   0x74, 0x6c, 0x65, 0x66, 0x69, 0x65, 0x6c, 0x64, 0x32, 0x64, 0x00])
    BF2_AVAILABLE_REPLY = bytearray([0xfe, 0xfd, 0x09, 0x00, 0x00, 0x00, 0x00])
    CHAL_VALIDATE = bytearray(
        [0x72, 0x62, 0x75, 0x67, 0x4a, 0x34, 0x34, 0x64, 0x34, 0x7a, 0x2b, 0x66, 0x61, 0x78, 0x30, 0x2f, 0x74, 0x74,
         0x56, 0x56, 0x46, 0x64, 0x47, 0x62, 0x4d, 0x7a, 0x38, 0x41, 0x00])
    SERVER_DETAILS = bytearray([0x03])
    SERVER_PING = bytearray([0x08])
    SERVER_CHAL = bytearray([0x01])

    debug_mode = False
    home_host_ip = "46.101.221.26" #BF2Demo.com IP
    registered_servers = {}

    def __init__(self, host, port, db):
        super(ServerListRegister, self).__init__()
        self.host = host
        self.port = port
        self.db = db
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        # Start the server checker
        self.check_servers()

    def run(self):

        while True:
            message, address = self.sock.recvfrom(65535)
            if self.debug_mode:
                print "DEBUG: Address: " + str(address)
                print "DEBUG: Content: " + message

            if not self.get_server(address):
                # New connection
                if message == self.BF2_AVAILABLE_REQ:
                    self.debug("__ BF2 AVAILABLE __")
                    self.send_to_server(self.BF2_AVAILABLE_REPLY, address)

                if len(message) > 5 and message[0] == self.SERVER_DETAILS:
                    self.debug("__ SERVER CHAL SENT __")
                    # Server details coming in
                    server = GameServer(address, self.db, self.debug_mode)
                    self.add_server(server)

                    details = bytearray(message)[:5]
                    validation_challenge = bytearray([
                        0xfe, 0xfd, 0x01, details[0], details[1], details[2], details[3], 0x44, 0x3d, 0x73,
                        0x7e, 0x6a, 0x59, 0x30, 0x30, 0x37, 0x43, 0x39, 0x35, 0x41, 0x42, 0x42, 0x35, 0x37, 0x34,
                        0x43, 0x43, 0x00
                    ])

                    # Send the validation challenge
                    self.send_to_server(validation_challenge, server.address)
                pass

            else:
                # We know this guy
                if len(message) == 5 and message[0] == self.SERVER_PING:
                    # Server ping
                    self.debug("__ SERVER PING __")
                    server = self.get_server(address)
                    server.server_ping()

                if len(message) > 5 and message[0] == self.SERVER_DETAILS:
                    self.debug("__ SERVER DETAILS UPDATE __")
                    server = self.get_server(address)
                    details_all = bytearray(message)[5:]
                    server_details = details_all.split('\x00')
                    server.update_server_details(server_details)

                if len(message) > 5 and message[0] == self.SERVER_CHAL:
                    # Validation challenge response
                    self.debug("__ SERVER CHAL RESPONSE __")
                    details = bytearray(message)[:5]
                    server_chal_response = bytearray(message)[5:]

                    if server_chal_response == self.CHAL_VALIDATE:
                        all_good = bytearray([0xfe, 0xfd, 0x0a, details[0], details[1], details[2], details[3]])
                        self.send_to_server(all_good, address)
                        server = self.get_server(address)
                        server.server_validate()

    def send_to_server(self, buff, address):
        self.debug("Sending: " + buff)
        self.sock.sendto(buff, address)

    def get_server(self, address):
        return self.registered_servers.get(address)

    def add_server(self, server):
        self.registered_servers[server.address] = server

    def server_disconnect(self, address):
        self.debug("__ REMOVING SERVER ___")
        server_id = self.registered_servers.get(address).server_id
        self.db.delete_server(server_id)
        self.registered_servers.pop(address)

    def check_servers(self):
        threading.Timer(30, self.check_servers).start()
        for address, server in self.registered_servers.items():
            if not server.is_active():
                self.server_disconnect(address)

    def debug(self, string):
        if self.debug_mode:
            print "DEBUG: " + str(string)
