import time


class GameServer:
    server_id = None
    # server_ip, server_port, last_refresh and last_ping are only used by us and are not part of default vars.
    server_var_keys = ["server_ip", "server_port", "last_refresh", "last_ping", "localip0", "localip1",
                       "country", "hostname", "gamename", "gamever", "mapname", "gametype", "gamevariant", "natneg",
                       "numplayers", "maxplayers", "gamemode", "password", "timelimit", "roundtime", "hostport",
                       "bf2_dedicated", "bf2_anticheat", "bf2_os", "bf2_autorec", "bf2_d_idx", "bf2_d_dl", "bf2_voip",
                       "bf2_autobalanced", "bf2_friendlyfire", "bf2_tkmode", "bf2_startdelay", "bf2_spawntime",
                       "bf2_sponsortext", "bf2_sponsorlogo_url", "bf2_communitylogo_url", "bf2_scorelimit",
                       "bf2_ticketratio", "bf2_teamratio", "bf2_team1", "bf2_team2", "bf2_bots", "bf2_pure",
                       "bf2_mapsize", "bf2_globalunlocks", "bf2_fps", "bf2_plasma", "bf2_reservedslots",
                       "bf2_coopbotratio", "bf2_coopbotcount", "bf2_coopbotdiff", "bf2_novehicles"]

    def __init__(self, address, db, debug_mode):
        self.address = address
        self.server_ip = address[0]
        self.server_port = address[1]
        self.db = db
        self.debug_mode = debug_mode

        self.server_refresh()
        self.server_ping()
        self.validated = False

    def server_refresh(self):
        self.last_refresh = time.time()
        self.server_ping()

    def server_ping(self):
        self.last_ping = time.time()

    def server_validate(self):
        self.validated = True

    def server_save(self):
        if self.validated:
            # Get vars we have for this server
            server_vars = {key: value for key, value in self.__dict__.items() if
                           not key.startswith('__') and not callable(key)}
            # This will be the filtered list to be saved in DB
            server_vars_db = {}
            for key in self.server_var_keys:
                if key in server_vars:
                    server_vars_db[key] = str(server_vars[key])
            # Save or Update
            if self.server_id is not None:
                if self.debug_mode:
                    print "DEBUG: Updating server info on DB."
                self.db.update_server(self.server_id, server_vars_db)
            else:
                if self.debug_mode:
                    print "DEBUG: Saving server info on DB."
                self.server_id = self.db.add_server(server_vars_db)

    def is_active(self):
        return time.time() - self.last_ping <= 60

    def update_server_details(self, server_details):
        # Populating or Updating
        self.server_refresh()
        # Go through details
        for index in range(0, len(server_details)):
            if (server_details[index]) == "localip0":
                self.localip0 = server_details[index + 1]
                pass
            if (server_details[index]) == "gametype":
                self.gametype = server_details[index + 1]
                pass
            if (server_details[index]) == "localip1":
                self.localip1 = server_details[index + 1]
                pass
            if (server_details[index]) == "localport":
                self.localport = server_details[index + 1]
                pass
            if (server_details[index]) == "natneg":
                self.natneg = str(str(server_details[index + 1]))
                pass
            if (server_details[index]) == "statechanged":
                self.statechanged = str(str(server_details[index + 1]))
                pass
            if (server_details[index]) == "gamename":
                self.gamename = str(str(server_details[index + 1]))
                pass
            if (server_details[index]) == "hostname":
                self.hostname = str(str(server_details[index + 1]))
                pass
            if (server_details[index]) == "gamever":
                self.gamever = str(server_details[index + 1])
                pass
            if (server_details[index]) == "mapname":
                self.mapname = str(server_details[index + 1])
                pass
            if (server_details[index]) == "gamevariant":
                self.gamevariant = str(server_details[index + 1])
                pass
            if (server_details[index]) == "numplayers":
                self.numplayers = str(server_details[index + 1])
                pass
            if (server_details[index]) == "maxplayers":
                self.maxplayers = str(server_details[index + 1])
                pass
            if (server_details[index]) == "gamemode":
                self.gamemode = str(server_details[index + 1])
                pass
            if (server_details[index]) == "password":
                self.password = str(server_details[index + 1])
                pass
            if (server_details[index]) == "timelimit":
                self.timelimit = str(server_details[index + 1])
                pass
            if (server_details[index]) == "roundtime":
                self.roundtime = str(server_details[index + 1])
                pass
            if (server_details[index]) == "hostport":
                self.hostport = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_dedicated":
                self.bf2_dedicated = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_ranked":
                self.bf2_ranked = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_anticheat":
                self.bf2_anticheat = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_os":
                self.bf2_os = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_autorec":
                self.bf2_autorec = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_d_idx":
                self.bf2_d_idx = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_d_dl":
                self.bf2_d_dl = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_voip":
                self.bf2_voip = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_autobalanced":
                self.bf2_autobalanced = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_friendlyfire":
                self.bf2_friendlyfire = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_startdelay":
                self.bf2_startdelay = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_spawntime":
                self.bf2_spawntime = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_sponsortext":
                self.bf2_sponsortext = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_sponsorlogo_url":
                self.bf2_sponsorlogo_url = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_communitylogo_url":
                self.bf2_communitylogo_url = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_scorelimit":
                self.bf2_scorelimit = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_ticketratio":
                self.bf2_ticketratio = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_teamratio":
                self.bf2_teamratio = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_team1":
                self.bf2_team1 = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_team2":
                self.bf2_team2 = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_bots":
                self.bf2_bots = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_pure":
                self.bf2_pure = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_mapsize":
                self.bf2_mapsize = str(server_details[index + 1])
                pass
            if (server_details[index]) == "bf2_globalunlocks":
                self.bf2_globalunlocks = str(server_details[index + 1])
                pass
        # Details updated, attempt to save/update server on DB.
        self.server_save()
