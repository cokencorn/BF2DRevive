from Database.DBConfig import DBConfig
from Servers.SearchProvider import SearchProvider
from Servers.ClientManager import ClientManager
from Database.GamespyAccountDB import GamespyAccountDB


class AccountServer:
    def __init__(self):
        db = GamespyAccountDB(DBConfig.get_config())
        # Try setup accounts table if does not exist
        db.create_accounts_table()
        # Run servers
        ClientManager("0.0.0.0", 29900, db).start()
        SearchProvider("0.0.0.0", 29901, db).start()


AccountServer()
