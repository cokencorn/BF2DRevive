from Database.DatabaseDriver import DatabaseDriver


class GamespyAccountDB(DatabaseDriver):
    def __init__(self, config):
        DatabaseDriver.__init__(self, config)
        self.tables = {}

    def get_user(self, nick):
        query = ("SELECT * FROM accounts WHERE name = %s LIMIT 1")
        cursor = super(GamespyAccountDB, self).query(query, [nick])
        return cursor

    def get_user_by_id_session(self, id, session):
        query = ("SELECT * FROM accounts WHERE id = %s AND session = %s LIMIT 1")
        cursor = super(GamespyAccountDB, self).query(query, [id, session])
        return cursor

    def get_user_by_email_password(self, email, password):
        query = ("SELECT * FROM accounts WHERE email = %s AND password = %s LIMIT 1")
        cursor = super(GamespyAccountDB, self).query(query, [email, password])
        return cursor

    def get_user_by_nick_email_password(self, name, email, password):
        query = ("SELECT * FROM accounts WHERE name = %s AND email = %s AND password = %s LIMIT 1")
        cursor = super(GamespyAccountDB, self).query(query, [name, email, password])
        return cursor

    def create_user(self, nick, hash, email, country, lastip):
        query = ("INSERT INTO accounts(name, password, email, country, lastip) VALUES(%s, %s, %s, %s, %s)")
        result = super(GamespyAccountDB, self).query(query, [nick, hash, email.lower(), country, lastip])
        lastrow = result.lastrowid
        return lastrow

    def set_user_country(self, pid, country):
        query = ("UPDATE accounts SET country=%s WHERE id=%s")
        result = super(GamespyAccountDB, self).query(query, [country, pid])
        lastrow = result.lastrowid
        return lastrow

    def set_session(self, session, pid):
        query = ("UPDATE accounts SET session=%s WHERE id=%s")
        result = super(GamespyAccountDB, self).query(query, [session, pid])
        lastrow = result.lastrowid
        return lastrow

    def create_accounts_table(self):
        sql = (
            "CREATE TABLE `accounts` ("
            "`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
            "`name` VARCHAR(20) NOT NULL UNIQUE,"
            "`password` VARCHAR(32) NOT NULL,"
            "`email` VARCHAR(50) NOT NULL,"
            "`country` VARCHAR(4) NOT NULL,"
            "`lastip` VARCHAR(20) DEFAULT NULL,"
            "`session` VARCHAR(8) DEFAULT 0"
            ") DEFAULT CHARSET=latin1;")
        return super(GamespyAccountDB, self).execute(sql)
