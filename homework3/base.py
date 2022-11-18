import pytest

from builder import Builder


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        self.builder = Builder()

        if self.authorize:
            self.api_client.post_login()

    def get_active_campaign(self, campaign) -> str:
        campaign_id = campaign[0]
        return self.api_client.get_campaign(campaign_id)

    def segments_list(self) -> str:
        return self.api_client.get_all_segments_list()

    def create_campaign(self) -> str:
        company_data = self.builder.campaign()
        return self.api_client.post_create_special_campaign(company_data.name, company_data.text)

    def create_segment(self, group_id=None):
        segment_data = self.builder.segment()
        return self.api_client.post_create_segment(segment_data.name, group_id)

    def create_vk_group_data_source(self, group_link):
        group_id = self.api_client.get_group_id(group_link)
        return [self.api_client.post_create_vk_group_data_source(group_id), group_id]

    def delete_campaign(self, new_campaign):
        return self.api_client.post_delete_campaign(new_campaign[0])

    def delete_segment(self, new_segment):
        return self.api_client.post_delete_segment(new_segment[0])

    def delete_data_source(self, source_id):
        return self.api_client.delete_data_source(source_id)
