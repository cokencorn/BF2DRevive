from Database.DatabaseDriver import DatabaseDriver


class GamespyServerDB(DatabaseDriver):
    def __init__(self, config):
        DatabaseDriver.__init__(self, config)
        self.tables = {}

    def get_servers(self):
        query = ("SELECT * FROM servers")
        cursor = super(GamespyServerDB, self).query(query, None)
        return cursor

    def add_server(self, server_vars):
        query_params = []
        query_vals = []

        for key, value in server_vars.iteritems():
            query_params.append(key)
            query_vals.append(value)

        query_param_str = ""
        query_value_str = ""

        for val in query_params[:-1]:
            query_param_str += (str(val) + ", ")
            query_value_str += "%s, "
        else:
            query_param_str += str(query_params[-1])
            query_value_str += "%s"

        query = ("INSERT INTO servers(" + query_param_str + ") VALUES(" + query_value_str + ")")
        result = super(GamespyServerDB, self).query(query, query_vals)
        lastrow = result.lastrowid
        return lastrow

    def update_server(self, id, server_vars):

        query_params = []
        query_vals = []

        for key, value in server_vars.iteritems():
            query_params.append(key)
            query_vals.append(value)

        query_vals.append(id)
        query_param_str = ""

        for val in query_params[:-1]:
            query_param_str += (str(val) + "=%s, ")
        else:
            query_param_str += (str(query_params[-1]) + "=%s")

        query = ("UPDATE servers SET " + query_param_str + " WHERE id=%s")
        result = super(GamespyServerDB, self).query(query, query_vals)
        lastrow = result.lastrowid
        return lastrow

    def delete_server(self, id):
        query = ("DELETE FROM servers WHERE id = %s")
        cursor = super(GamespyServerDB, self).query(query, [id])
        return cursor

    def create_servers_table(self):
        sql = (
            "CREATE TABLE `servers` ("
            "`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
            "`server_ip` VARCHAR(50) NOT NULL,"
            "`server_port` VARCHAR(50) NOT NULL,"
            "`last_refresh` VARCHAR(20) DEFAULT NULL,"
            "`last_ping` VARCHAR(20) DEFAULT NULL,"
            "`localip0` VARCHAR(50) DEFAULT NULL,"
            "`localip1` VARCHAR(50) DEFAULT NULL,"
            "`country` VARCHAR(2) DEFAULT NULL,"
            "`hostname` VARCHAR(150) DEFAULT NULL,"
            "`gamename` VARCHAR(20) DEFAULT NULL,"
            "`gamever` VARCHAR(20) DEFAULT NULL,"
            "`mapname` VARCHAR(50) DEFAULT NULL,"
            "`gametype` VARCHAR(20) DEFAULT NULL,"
            "`gamevariant` VARCHAR(20) DEFAULT NULL,"
            "`numplayers` VARCHAR(10) DEFAULT NULL,"
            "`maxplayers` VARCHAR(10) DEFAULT NULL,"
            "`gamemode` VARCHAR(20) DEFAULT NULL,"
            "`password` VARCHAR(30) DEFAULT NULL,"
            "`timelimit` VARCHAR(10) DEFAULT NULL,"
            "`roundtime` VARCHAR(10) DEFAULT NULL,"
            "`hostport` VARCHAR(50) DEFAULT NULL,"
            "`natneg` VARCHAR(1) DEFAULT '0',"
            "`bf2_dedicated` VARCHAR(1) DEFAULT '0',"
            "`bf2_anticheat` VARCHAR(1) DEFAULT '0',"
            "`bf2_ranked` VARCHAR(1) DEFAULT '0',"
            "`bf2_os` VARCHAR(10) DEFAULT NULL,"
            "`bf2_autorec` VARCHAR(1) DEFAULT NULL,"
            "`bf2_d_idx` VARCHAR(20) DEFAULT NULL,"
            "`bf2_d_dl` VARCHAR(20) DEFAULT NULL,"
            "`bf2_voip` VARCHAR(1) DEFAULT NULL,"
            "`bf2_autobalanced` VARCHAR(1) DEFAULT '0',"
            "`bf2_friendlyfire` VARCHAR(1) DEFAULT '0',"
            "`bf2_tkmode` VARCHAR(20) DEFAULT NULL,"
            "`bf2_startdelay` VARCHAR(2) DEFAULT NULL,"
            "`bf2_spawntime` VARCHAR(10) DEFAULT NULL,"
            "`bf2_sponsortext` VARCHAR(850) DEFAULT NULL,"
            "`bf2_sponsorlogo_url` VARCHAR(250) DEFAULT NULL,"
            "`bf2_communitylogo_url` VARCHAR(250) DEFAULT NULL,"
            "`bf2_scorelimit` VARCHAR(10) DEFAULT NULL,"
            "`bf2_ticketratio` VARCHAR(10) DEFAULT NULL,"
            "`bf2_teamratio` VARCHAR(10) DEFAULT NULL,"
            "`bf2_team1` VARCHAR(10) DEFAULT NULL,"
            "`bf2_team2` VARCHAR(10) DEFAULT NULL,"
            "`bf2_bots` VARCHAR(1) DEFAULT '0',"
            "`bf2_pure` VARCHAR(1) DEFAULT '0',"
            "`bf2_mapsize` VARCHAR(10) DEFAULT NULL,"
            "`bf2_globalunlocks` VARCHAR(1) DEFAULT '0',"
            "`bf2_fps` VARCHAR(10) DEFAULT '0',"
            "`bf2_plasma` VARCHAR(1) DEFAULT '0',"
            "`bf2_reservedslots` VARCHAR(10) DEFAULT '0',"
            "`bf2_coopbotratio` VARCHAR(10) DEFAULT '0',"
            "`bf2_coopbotcount` VARCHAR(10) DEFAULT '0',"
            "`bf2_coopbotdiff` VARCHAR(10) DEFAULT '0',"
            "`bf2_novehicles` VARCHAR(1) DEFAULT '0'"
            ") DEFAULT CHARSET=latin1;")
        return super(GamespyServerDB, self).execute(sql)
