import threading

from Database.DBConfig import DBConfig
from Database.GamespyServerDB import GamespyServerDB
from Servers.ServerListRegister import ServerListRegister
from Servers.ServerListProvider import ServerListProvider


def main():
    db = GamespyServerDB(DBConfig.get_config())
    # Try setup accounts table if does not exist
    db.create_servers_table()
    # Run servers
    sr = ServerListRegister("0.0.0.0", 27900, db)
    sr.start()
    sp = ServerListProvider("0.0.0.0", 28910, db)
    sp.start()
    sp.join()


main_thread = threading.Thread(target=main)
main_thread.start()
main_thread.join()
