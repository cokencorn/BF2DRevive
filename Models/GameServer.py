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

        self.last_ping = None
        self.last_refresh = None

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
                    print ("DEBUG: Updating server info on DB.")
                self.db.update_server(self.server_id, server_vars_db)
            else:
                if self.debug_mode:
                    print ("DEBUG: Saving server info on DB.")
                self.server_id = self.db.add_server(server_vars_db)

    def is_active(self):
        return time.time() - self.last_ping <= 60

    def update_server_details(self, server_details):
        # Populating or Updating
        self.server_refresh()

        # Mapping keys to attributes
        attributes = {
            "localip0": "localip0",
            "gametype": "gametype",
            "localip1": "localip1",
            "localport": "localport",
            "natneg": "natneg",
            "statechanged": "statechanged",
            "gamename": "gamename",
            "hostname": "hostname",
            "gamever": "gamever",
            "mapname": "mapname",
            "gamevariant": "gamevariant",
            "numplayers": "numplayers",
            "maxplayers": "maxplayers",
            "gamemode": "gamemode",
            "password": "password",
            "timelimit": "timelimit",
            "roundtime": "roundtime",
            "hostport": "hostport",
            "bf2_dedicated": "bf2_dedicated",
            "bf2_ranked": "bf2_ranked",
            "bf2_anticheat": "bf2_anticheat",
            "bf2_os": "bf2_os",
            "bf2_autorec": "bf2_autorec",
            "bf2_d_idx": "bf2_d_idx",
            "bf2_d_dl": "bf2_d_dl",
            "bf2_voip": "bf2_voip",
            "bf2_autobalanced": "bf2_autobalanced",
            "bf2_friendlyfire": "bf2_friendlyfire",
            "bf2_startdelay": "bf2_startdelay",
            "bf2_spawntime": "bf2_spawntime",
            "bf2_sponsortext": "bf2_sponsortext",
            "bf2_sponsorlogo_url": "bf2_sponsorlogo_url",
            "bf2_communitylogo_url": "bf2_communitylogo_url",
            "bf2_scorelimit": "bf2_scorelimit",
            "bf2_ticketratio": "bf2_ticketratio",
            "bf2_teamratio": "bf2_teamratio",
            "bf2_team1": "bf2_team1",
            "bf2_team2": "bf2_team2",
            "bf2_bots": "bf2_bots",
            "bf2_pure": "bf2_pure",
            "bf2_mapsize": "bf2_mapsize",
            "bf2_globalunlocks": "bf2_globalunlocks"
        }

        # Go through details
        for index in range(0, len(server_details), 2):
            key = server_details[index].decode('utf-8')
            value = server_details[index + 1].decode('utf-8')
            if key in attributes:
                setattr(self, attributes[key], value)

        # Details updated, attempt to save/update server on DB.
        self.server_save()