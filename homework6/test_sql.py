import pytest
from client import MysqlClient


class TestMysql:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, parsed_info):
        self.client: MysqlClient = mysql_client
        self.info = parsed_info

    def test_requests_amount(self, setup):
        self.client.write_amount_to_table(info=self.info, info_name='requests_amount',
                                          table_name='requests_amount')
        assert len(self.client.get_table('requests_amount')) == 1

    def test_requests_amount_by_type(self, setup):
        self.client.write_data_to_requests_amount_by_type_table(info=self.info)
        assert len(self.client.get_table('requests_amount_by_type')) == 5

    def test_most_frequent_requests(self, lines_amount=10):
        self.client.write_most_frequent_requests(lines_amount=lines_amount, info=self.info)
        assert len(self.client.get_table('most_frequent_requests')) == lines_amount

    def test_highest_request_with_4xx_code(self, lines_amount=5):
        self.client.write_highest_request_with_4xx_code(lines_amount=lines_amount, info=self.info)
        assert len(self.client.get_table('highest_request_with_4XX_code')) == lines_amount

    def test_most_frequent_users(self, lines_amount=5):
        self.client.write_most_frequent_users_with_5xx_code(lines_amount=lines_amount, info=self.info)
        assert len(self.client.get_table('most_frequent_users_with_5XX_code')) == lines_amount
