import threading

from Database.DBConfig import DBConfig
from Servers.SearchProvider import SearchProvider
from Servers.ClientManager import ClientManager
from Database.GamespyAccountDB import GamespyAccountDB


def main():
    db = GamespyAccountDB(DBConfig.get_config())
    # Try setup accounts table if does not exist
    db.create_accounts_table()

    # Run servers
    cm = ClientManager("0.0.0.0", 29900, db)
    cm.start()
    sp = SearchProvider("0.0.0.0", 29901, db)
    sp.start()
    sp.join()


main_thread = threading.Thread(target=main)
main_thread.start()
main_thread.join()
