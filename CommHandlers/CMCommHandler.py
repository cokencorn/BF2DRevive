import hashlib
import random
import string
from Utils.Gamespy import Gamespy


class CMCommHandler:
    # This class handles all client manager communications with the game client.
    debug_mode = False

    def prepare_proof(self, query, connection):

        checks = 0
        if 'uniquenick' in query:
            connection.uniquenick = query['uniquenick']
            checks += 1
        if 'challenge' in query:
            connection.client_challenge = query['challenge']
            checks += 1
        if 'response' in query:
            connection.client_response = query['response']
            checks += 1

        if checks != 3:
            print("Checks passed: " + str(checks) + "/3")
            print('Proof checks failed. Invalid client query.')
            print(query)
            connection.send_to_client(self.invalid_query())

        # Check if we know the player
        if connection.check_user():
            if connection.client_response == self.generate_resonse(connection):
                query_string = "\\lc\\2\\sesskey\\{0}\\proof\\{1}\\userid\\{2}\\profileid\\" + \
                               "{2}\\uniquenick\\{3}\\lt\\{4}__\\id\\1\\final\\"

                query_string = query_string.format(
                    connection.session_start(),
                    self.generate_proof(connection),
                    connection.pid,
                    connection.uniquenick,
                    self.random_string(22)
                )

                self.debug("Client with username (" + connection.uniquenick + ") logging in.")
                connection.send_to_client(query_string)
            else:
                connection.send_to_client(self.invalid_query("The password provided is incorrect.", 260))
        else:
            connection.send_to_client(self.invalid_query("Username " + query['uniquenick'] + " is not  registered with "
                                                         + "BF2Demo.com servers.", 265))

    def new_user(self, query, connection):

        if set(("nick", "email", "passwordenc")) <= set(query):
            connection.nick = query['nick']
            connection.passwordenc = query['passwordenc']
            connection.email = query['email']
            # Check if user is already registered
            if connection.check_user():
                connection.send_to_client(self.invalid_query("This account name is already in use. " +
                                                             " Please try another name."))
            else:
                password = Gamespy.decode_password(connection.passwordenc)
                connection.password = hashlib.md5(password.encode()).hexdigest()
                self.debug("Registering a new user")

                pid = connection.db.create_user(connection.nick, connection.password,
                                                connection.email, connection.country, connection.address[0])
                connection.send_to_client("\\nur\\userid\\" + str(pid) + "\\profileid\\" + str(pid) +
                                          "\\id\\1\\final\\")

        else:
            print("Invalid query during registration attempt.")
            print(query)
            connection.send_to_client(self.invalid_query())

    def get_profile(self, query, connection):

        if "sesskey" not in query or "profileid" not in query:
            connection.send_to_client(self.invalid_query())
            return

        # Renew session to ensure validity
        connection.session = query["sesskey"]
        users = connection.db.get_user_by_id_session(connection.pid, connection.session)

        if users.rowcount == 0:
            connection.send_to_client(self.invalid_query("Unable to get any associated player profiles.", 551))
            return

        # Get first row from cursor
        user = users.fetchone()
        query_string = "\\pi\\\\profileid\\{0}\\nick\\{1}\\userid\\{0}\\email\\{2}\\sig\\{3}\\uniquenick\\" + \
                       "{1}\\pid\\0\\firstname\\\\lastname\\countrycode\\{4}\\birthday\\16844722\\" + \
                       "lon\\0.000000\\lat\\0.000000\\loc\\id\\{5}\\\\final\\"

        query_id = int(query['id'])
        query_string = query_string.format(connection.pid, user['name'], user['email'], self.generate_sig(),
                                           user['country'],
                                           2 if query_id == 2 else 5)

        self.debug("Client with username (" + connection.uniquenick + ") requested profile information.")
        connection.send_to_client(query_string)

    def update_profile(self, query, connection):

        country = "??"
        if "countrycode" in query:
            country = query["countrycode"]

        connection.db.set_user_country(connection.pid, country)

    def nicks(self, query, connection):

        if "email" not in query or ("passenc" not in query and "pass" not in query):
            connection.send_to_client(self.invalid_query())

        if "passenc" in query:
            password = Gamespy.decode_password(query["passenc"])
        elif "pass" in query:
            password = query["pass"]

        connection.email = query["email"]
        connection.password = hashlib.md5(password.encode()).hexdigest()
        users = connection.db.get_user_by_email_password(connection.email, connection.password)

        # if not user:
        #    connection.send_to_client(self.invalid_query("Unable to get any associated player profiles.", 551))
        #    return
        connection.send_to_client(self.prepare_nicks(users))

    def check(self, query, connection):
        nick = None

        if "email" not in query or "pass" not in query:
            connection.send_to_client(self.invalid_query())
            return

        if "uniquenick" in query:
            nick = query["uniquenick"]

        if not nick and "nick" in query:
            nick = query["nick"]

        if not nick:
            connection.send_to_client(self.invalid_query())
            return

        connection.nick = nick
        connection.email = query["email"]
        connection.password = hashlib.md5(query["pass"].encode()).hexdigest()

        # Validate everything we have
        user = connection.db.get_user_by_nick_email_password(connection.nick, connection.email, connection.password)
        if user.rowcount == 0:
            connection.send_to_client(self.invalid_query("Username " + nick + " doesn't exist!", 265))
            return

        connection.send_to_client("\\cur\\0\\pid\\{0}\\final\\".format(connection.pid))

    def generate_proof(self, connection):
        hash_string = connection.password
        hash_string += ' ' * 48
        hash_string += connection.uniquenick
        hash_string += connection.server_challenge
        hash_string += connection.client_challenge
        hash_string += connection.password
        return hashlib.md5(hash_string.encode()).hexdigest()

    def generate_resonse(self, connection):
        hash_string = connection.password
        hash_string += ' ' * 48
        hash_string += connection.uniquenick
        hash_string += connection.client_challenge
        hash_string += connection.server_challenge
        hash_string += connection.password
        return hashlib.md5(hash_string.encode()).hexdigest()

    def generate_sig(self):
        return hashlib.md5(self.random_string(32).encode()).hexdigest()

    def invalid_query(self, message="Invalid Query!", err_code=0):
        return '\\error\\err\\' + str(err_code) + '\\fatal\\\\errmsg\\' + message + '\\id\\1\\final\\'

    def random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

    def prepare_nicks(self, users):
        message = "\\nr\\" + str(users.rowcount)
        for user in users:
            message += "\\nick\\{0}\\uniquenick\\{0}".format(user['name'])
        message += "\\ndone\\\\final\\"
        return message

    def debug(self, string):
        if self.debug_mode:
            print("DEBUG: " + str(string))
