import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MysqlClient:

    def __init__(self, user, password, db_name):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self):
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine, autocommit=True, autoflush=True)
        self.session = session()

    def execute_query(self, query, parse=False):
        res = self.connection.execute(query)
        if parse:
            return res.mappings().all()
