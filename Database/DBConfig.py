class DBConfig:
    DATABASE_NAME = "bf2"
    DATABASE_USER = "root"
    DATABASE_PASS = ""
    DATABASE_HOST = "127.0.0.1"

    @staticmethod
    def get_config():
        return {
            'user': DBConfig.DATABASE_USER,
            'password': DBConfig.DATABASE_PASS,
            'host': DBConfig.DATABASE_HOST,
            'ssl_disabled': True,
        }
