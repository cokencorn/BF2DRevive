import threading
from threading import Thread
from random import choice
from CommHandlers.CMCommHandler import CMCommHandler
import time
import string
import socket
import errno


class AccountConnection(Thread):
    debug_mode = False
    active = True
    # IP : Port Pair
    address = None
    socket = None
    # Parent Server
    parent = None
    server_challenge = None
    client_response = None
    client_challenge = None
    comm_handler = None

    # Player Details
    pid = 0
    session = 0
    nick = None
    email = None
    uniquenick = None
    passwordenc = None
    password = None
    country = '??'

    def __init__(self, parent, address, socket, db):
        super(AccountConnection, self).__init__()
        self.address = address
        self.socket = socket
        self.parent = parent
        self.db = db

    def run(self):

        if self.is_parent_cm():
            # Start keep alive requests
            self.send_keep_alive(False)
            # Send server challenge
            self.send_to_client(self.generate_server_challenge())

        while self.active:
            buff = self.receive_from_client()
            if buff:
                self.debug("Received: " + str(buff))
                # Handle response
                self.handle_response(buff)
            else:
                # No need to run SP thread. It's on-demand
                if not self.is_parent_cm():
                    self.disconnect()

    def receive_from_client(self):
        time.sleep(1)
        try:
            return self.socket.recv(8192)
        except socket.error as exc:
            if exc.errno == errno.ECONNRESET:
                # Connection reset by peer
                self.disconnect()
                return
            if int(exc.errno) == int(10054):
                # An existing connection was forcibly closed by the remote host
                self.disconnect()
                return
            if exc.errno == int(110):
                # Timeout..
                self.disconnect()
                return
            # Anything else, we print
            print("RECV Socket error: %s" % exc)
            self.disconnect()

    def prep_buffer_before_send(self, data):
        # This converts string to bytes
        buffer_data = bytearray()
        buffer_data.extend(data.encode())
        return buffer_data

    def send_to_client(self, buff):
        self.debug("Sending: " + str(buff))
        try:
            self.socket.send(self.prep_buffer_before_send(buff))
        except socket.error as exc:
            if exc.errno == errno.EPIPE:
                # Broken Pipe - 32
                self.disconnect()
                return
            if exc.errno == int(104):
                # Connection reset by peer
                self.disconnect()
            print("SEND Socket error: %s" % exc)
            self.disconnect()

    def prep_error_message(self, message):
        return '\\error\\err\\0\\fatal\\errmsg\\' + message + '\\id\\1\\final\\'

    def generate_server_challenge(self):
        self.server_challenge = "".join(choice(string.ascii_lowercase) for i in range(10))
        return '\\lc\\1\\challenge\\' + self.server_challenge + '\\id\\1\\final\\'

    def client_query_to_dic(self, response):
        temp_list = response.split(b'\\')
        # skip 1st and final element, they are empty
        return {temp_list[i].decode(): temp_list[i + 1].decode() for i in range(1, len(temp_list) - 1, 2)}

    def handle_response(self, buff):
        # Prepare query
        query = self.client_query_to_dic(buff)
        if not self.comm_handler:
            self.comm_handler = CMCommHandler()

        if self.is_parent_cm():
            if 'login' in query:
                if self.validate_request(query):
                    self.comm_handler.prepare_proof(query, self)

            elif 'newuser' in query:
                if self.validate_request(query):
                    self.comm_handler.new_user(query, self)

            elif 'getprofile' in query:
                self.comm_handler.get_profile(query, self)

            elif 'updatepro' in query:
                self.comm_handler.update_profile(query, self)

            elif 'logout' in query:
                self.disconnect()

            else:
                self.unknown_query(buff)

        else:
            if 'nicks' in query:
                if self.validate_request(query):
                    self.comm_handler.nicks(query, self)

            elif 'check' in query:
                if self.validate_request(query):
                    self.comm_handler.check(query, self)
            else:
                self.unknown_query(buff)

    def validate_request(self, query):
        if ('gamename' not in query) or (query["gamename"] != "battlefield2d"):
            print("Gamename not correct. Invalid query from a client. Dropping.")
            return False
        return True

    def is_parent_cm(self):
        return True if self.parent.type == "CM" else False

    def disconnect(self):
        if self.is_parent_cm() and self.session != 0:
            self.parent.client_disconnect(self)
        self.socket.close()
        # Remove active session
        if self.pid is not None:
            self.db.set_session(0, self.pid)
        self.active = False

    def unknown_query(self, query):
        print("Unknown Query: " + str(query))

    def session_start(self):
        # Get a new session
        self.session = self.parent.generate_session()
        self.db.set_session(self.session, self.pid)
        return self.session

    def check_user(self):
        nick = self.uniquenick or self.nick
        users = self.db.get_user(nick)
        if users.rowcount == 0:
            return False
        # Set user details
        user = users.fetchone()
        self.pid = user['id']
        self.password = user['password']
        return True

    def send_keep_alive(self, start_now=True):
        if self.active:
            self.debug("KA Request begin")
            if start_now:
                self.debug("Sending keep alive to: " + str(self.uniquenick or self.nick))
                self.send_to_client('\\ka\\\\final\\')
            if self.active:
                self.debug("Sending keep alive (45 seecond check) to: " + str(self.uniquenick or self.nick))
                # Send every 45 seconds to check if client is still with us.
                threading.Timer(45, self.send_keep_alive).start()

    def debug(self, string):
        if self.debug_mode:
            print("DEBUG: " + str(string))
