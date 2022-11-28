import sqlalchemy
from sqlalchemy.orm import sessionmaker
from orm.models import *


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

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def create_table(self, table_name):
        if not sqlalchemy.inspect(self.engine).has_table(table_name):
            Base.metadata.tables[table_name].create(self.engine)

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def write_amount_to_table(self, info, info_name, table_name):
        self.execute_query(f'insert into {table_name} '
                           f'(`data_name`, `amount`) values ("{info_name}", "{info[info_name]}")')

    def write_data_to_requests_amount_by_type_table(self, info):
        self.write_amount_to_table(info=info, info_name='get_requests_amount',
                                   table_name='requests_amount_by_type')
        self.write_amount_to_table(info=info, info_name='post_requests_amount',
                                   table_name='requests_amount_by_type')
        self.write_amount_to_table(info=info, info_name='head_requests_amount',
                                   table_name='requests_amount_by_type')
        self.write_amount_to_table(info=info, info_name='put_requests_amount',
                                   table_name='requests_amount_by_type')
        self.write_amount_to_table(info=info, info_name='other_requests_amount',
                                   table_name='requests_amount_by_type')

    def write_most_frequent_requests(self, lines_amount, info):
        items_list = list(info['most_frequent_requests'].items())
        for i in range(lines_amount):
            self.execute_query(f'insert into most_frequent_requests '
                               f'(`url`, `amount`) values ("{items_list[i][0]}", "{items_list[i][1]}")')

    def write_most_frequent_users_with_5xx_code(self, lines_amount, info):
        items_list = list(info['five_frequent_users_with_5XX_code_dict'].items())
        for i in range(lines_amount):
            self.execute_query(f'insert into most_frequent_users_with_5XX_code '
                               f'(`ip_address`, `amount`) values ("{items_list[i][0]}", "{items_list[i][1]}")')

    def write_highest_request_with_4xx_code(self, lines_amount, info):
        items_list = list(info['five_highest_request_with_4XX_code_dict'].items())
        for i in range(lines_amount):
            self.execute_query(f'insert into highest_request_with_4XX_code '
                               f'(`url`, `exit_code`, `size`, `ip_address`) '
                               f'values ("{items_list[i][0].split()[0].replace("%", "%%")}", '
                               f'"{items_list[i][0].split()[1]}", '
                               f'"{items_list[i][1].split()[0]}", '
                               f'"{items_list[i][1].split()[1]}")')

    def get_requests_amount(self, **filters):
        self.session.commit()
        return self.session.query(RequestsAmountModel).filter_by(**filters).all()

    def get_requests_amount_by_type(self, **filters):
        self.session.commit()
        return self.session.query(RequestsAmountByTypeModel).filter_by(**filters).all()

    def get_most_frequent_requests(self, **filters):
        self.session.commit()
        return self.session.query(MostFrequentRequestsModel).filter_by(**filters).all()

    def get_highest_request_with_4xx_code(self, **filters):
        self.session.commit()
        return self.session.query(HighestRequestWith4XXCodeModel).filter_by(**filters).all()

    def get_most_frequent_users_with_5xx_code(self, **filters):
        self.session.commit()
        return self.session.query(MostFrequentUsersWith5XXCodeModel).filter_by(**filters).all()
