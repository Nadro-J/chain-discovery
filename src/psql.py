import psycopg2

class connector:
    def __init__(self, config):
        self.config = config
        self.user   = self.config['user']
        self.passwd = self.config['password']
        self.host   = self.config['host']
        self.port   = self.config['port']
        self.db     = self.config['database']

        # PostgreSQL connection details
        self.connection = psycopg2.connect(
            user        = self.user,
            password    = self.passwd,
            host        = self.host,
            port        = self.port,
            database    = self.db
        )

        self.cursor     = self.connection.cursor()