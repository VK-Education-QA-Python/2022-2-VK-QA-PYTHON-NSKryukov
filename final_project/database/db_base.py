import pytest
from database.mysql_client import MysqlClient
from database.models.base_model import *


class MySqlBase:

    @pytest.fixture(scope='function', autouse=True)
    def db_setup(self, mysql_client):
        self.mysql_client: MysqlClient = mysql_client

    def get_table(self, **filters):
        return self.mysql_client.session.query(TestModel).filter_by(**filters).all()
