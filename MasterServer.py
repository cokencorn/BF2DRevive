from Database.DBConfig import DBConfig
from Database.GamespyServerDB import GamespyServerDB
from Servers.ServerListRegister import ServerListRegister
from Servers.ServerListProvider import ServerListProvider


class MasterServer:
    def __init__(self):
        db = GamespyServerDB(DBConfig.get_config())
        # Try setup accounts table if does not exist
        db.create_servers_table()
        # Run servers
        ServerListRegister("0.0.0.0", 27900, db).start()
        ServerListProvider("0.0.0.0", 28910, db).start()


MasterServer()
