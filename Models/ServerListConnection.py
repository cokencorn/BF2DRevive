import socket
import time
import errno
import struct
from threading import Thread
from Utils.Enctypex import Enctypex


class ServerListConnection(Thread):
    debug_mode = True
    MS_REQ = bytearray("\x00\x00\x00\x00", encoding='utf8')
    # DO NOT TOUCH!
    active = True

    def __init__(self, parent, address, socket, db):
        super(ServerListConnection, self).__init__()
        self.parent = parent
        self.address = address
        self.socket = socket
        self.db = db

    def run(self):
        while self.active:
            buff = self.receive_from_client()
            if buff:
                self.debug("Received: " + str(buff))
                if bytearray(buff).endswith(self.MS_REQ):
                    buff = buff.split(b"battlefield2d\x00battlefield2d")
                    if buff[1]:
                        self.parse_request(buff[1].decode()[1:])
            else:
                self.active = False

    def receive_from_client(self):
        time.sleep(1)
        try:
            return self.socket.recv(8192)
        except socket.error as exc:
            if exc.errno == errno.ECONNRESET:
                # Too frequent requests causes this, drop them
                self.debug("Client disconnected. Code: 10054")
                self.active = False
                return
            print("SL - RECV Socket error: %s" % exc)
            self.active = False

    def prep_buffer_before_send(self, data):
        # This converts string to bytes (array)
        buffer_data = bytearray()
        buffer_data.extend(data)
        return buffer_data

    def send_to_client(self, buff):
        self.debug("Sending: " + str(buff))
        try:
            self.socket.send(self.prep_buffer_before_send(buff))
        except socket.error as exc:
            print("SL - SEND Socket error: %s" % exc)
            pass

    def parse_request(self, data):

        data = data.split('\x00')
        validator = data[0][:8]
        filters = data[0][8:]
        fields = list(filter(None, data[1].split('\\')))

        # GSEncode the query
        encoded_query = Enctypex.encode(
            bytearray("hW6m9a".encode()),  # Battlefield 2 Handoff Key
            bytearray(validator.encode()),
            self.pack_server_list(filters, fields)
        )
        # Send it to client
        self.send_to_client(encoded_query)

    def pack_server_list(self, filters, fields):
        # We currently do not care about filters
        # Remove empty strings
        fields = list(filter(None, fields))
        data = bytearray()
        # Get IP bytes
        data.extend(socket.inet_aton(self.address[0]))
        data.extend([25, 100])  # Port
        data.extend([21])  # Fields length
        data.extend([0])  # End

        for index in range(0, len(fields)):
            if len(fields[index]) > 0:
                data.extend(fields[index].encode())
                data.extend([0, 0])

        # Server Loop - BEGIN
        for server in self.db.get_servers():

            data.append(81)
            data.extend(socket.inet_aton(server['server_ip']))  # IP Bytes
            query_port = struct.pack('>H', int(server['server_port']))
            data.extend(struct.unpack('>BB', query_port))  # Port Bytes
            data.extend([255])  # End

            for i in range(0, len(fields)):
                if fields[i] in server:
                    # Unicode to string conversion
                    data.extend(str(server[fields[i]]).encode())
                    if i < len(fields) - 1:
                        data.extend([0, 255])

            # Server separator
            data.append(0)
        # Server Loop - END
        data.extend([0, 255, 255, 255, 255])
        return data

    def debug(self, string):
        if self.debug_mode:
            print("DEBUG: " + str(string))
