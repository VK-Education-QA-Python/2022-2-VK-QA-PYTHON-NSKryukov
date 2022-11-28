import pytest

from base import ApiBase


@pytest.mark.API
class TestApi(ApiBase):
    def test_create_and_delete_campaign(self):
        new_campaign = self.create_campaign()
        assert new_campaign == self.get_active_campaign(new_campaign)
        self.delete_campaign(new_campaign)

    def test_create_and_delete_segment(self):
        new_segment = self.create_segment()
        assert new_segment in self.segments_list()
        self.delete_segment(new_segment)

    def test_create_and_delete_segment_vk_source(self):
        new_source = self.create_vk_group_data_source('https://vk.com/vkedu')
        new_source_group_id = new_source[1]
        new_source_id = new_source[0]
        new_segment = self.create_segment(new_source_group_id)
        assert new_segment in self.segments_list()
        self.delete_segment(new_segment)
        self.delete_data_source(new_source_id)
