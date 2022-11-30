import pytest
from client import MysqlClient
from python_parser import ParsedLogs

tables_list = ['requests_amount', 'requests_amount_by_type', 'most_frequent_requests',
               'highest_request_with_4XX_code', 'most_frequent_users_with_5XX_code']


def pytest_configure(config):
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        for i in tables_list:
            mysql_client.create_table(i)
    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client

    client.connection.close()


@pytest.fixture(scope='session')
def parsed_info() -> dict:
    logs_object = ParsedLogs()
    return logs_object.get_info()
