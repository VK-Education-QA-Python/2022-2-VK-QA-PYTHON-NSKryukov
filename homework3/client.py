import requests
from datetime import date
import json


class ApiClient:

    def __init__(self):
        self.cookies = None
        self.headers = None

        self.login = 'test_nskryukov@mail.ru'
        self.password = 'secretpool'

        self.session = requests.Session()

    def post_login(self):
        data = {
            'login': self.login,
            'password': self.password,
            'continue': 'https://target-sandbox.my.com/auth/mycom',
            'failure': 'https://account.my.com/login/'
        }

        headers = {
            'Referer': 'https://target-sandbox.my.com/'
        }

        self.session.post(url='https://auth-ac.my.com/auth', headers=headers, data=data) # mc csrf_token mcru
        self.session.get(url='https://target-sandbox.my.com/csrf/', cookies=self.session.cookies)

        self.cookies = self.session.cookies
        self.headers = {
            'X-CSRFToken': f'{self.cookies["csrftoken"]}'
        }

    def post_create_special_campaign(self, unique_name=None, text=None) -> tuple[int, str]:
        package_id = self.get_package_id('special')[0]
        link_id = self.get_id_of_link('https://education.vk.company/')

        data = {"name": unique_name,
                "objective": "special",
                "package_id": package_id,
                "banners": [{"textblocks": {"billboard_video": {"text": text}}, "urls": {"primary": {"id": link_id}},
                             "name": ""}]
                }

        request = self.session.post(url='https://target-sandbox.my.com/api/v2/campaigns.json', data=json.dumps(data),
                                    headers=self.headers, cookies=self.cookies)
        created_campaign = (int(request.content.decode('utf-8').split(':')[-1][1:-1]), unique_name)

        return created_campaign

    def post_create_segment(self, unique_name, group_id=None):
        if group_id:
            relations = [{"object_type": "remarketing_vk_group", "params": {"source_id": group_id,
                                                                            "type": "positive"}}]
        else:
            relations = [{"object_type": "remarketing_game_player", "params": {"game": "warfacemailru",
                                                                               "type": "positive",
                                                                               "left": 365,
                                                                               "right": 0}}]

        data = {
            "name": unique_name,
            "pass_condition": 1,
            "relations": relations
        }

        request = self.session.post(url='https://target-sandbox.my.com/api/v2/remarketing/segments.json',
                                    headers=self.headers, cookies=self.cookies, data=json.dumps(data))
        created_segment = (int(request.content.decode('utf-8').split(':')[-1][1:-1]), unique_name)

        return created_segment

    def post_create_vk_group_data_source(self, group_id) -> int:
        data = {"items": [{"object_id": group_id}]}

        request = self.session.post(url='https://target-sandbox.my.com/api/v2/remarketing/vk_groups/bulk.json',
                                    headers=self.headers, cookies=self.cookies, data=json.dumps(data))

        return json.loads(request.content)['items'][0]['id']

    def get_group_id(self, group_link) -> int:
        request = self.session.get(url='https://target-sandbox.my.com/api/v2/vk_groups.json',
                                   cookies=self.cookies, params=f'_q={group_link}')

        return json.loads(request.content)['items'][0]['id']

    def get_campaign(self, campaign_id) -> tuple[int, str]:
        response = self.session.get(url='https://target-sandbox.my.com/api/v2/campaigns.json',
                                    cookies=self.cookies, params=f'_id__in={campaign_id}')
        return tuple(response.json()['items'][0].values())[0:-1]

    def get_all_segments_list(self) -> list[tuple[int, str]]:
        response = self.session.get(url='https://target-sandbox.my.com/api/v2/remarketing/segments.json',
                                    cookies=self.cookies)

        segments_list = []
        for i in json.loads(response.content)['items']:
            segments_list.append((i['id'], i['name']))

        return segments_list

    def post_delete_campaign(self, campaign_id):
        data = {
            'status': 'deleted'
        }

        request = self.session.post(url=f'https://target-sandbox.my.com/api/v2/campaigns/{campaign_id}.json',
                                    headers=self.headers, cookies=self.cookies, data=json.dumps(data))

        return request.status_code

    def post_delete_segment(self, segment_id):
        request = self.session.delete(
                                    url=f'https://target-sandbox.my.com/api/v2/remarketing/segments/{segment_id}.json',
                                    headers=self.headers, cookies=self.cookies)
        return request.status_code

    def delete_data_source(self, source_id):
        request = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/vk_groups/{source_id}.json', headers=self.headers,
            cookies=self.cookies)

        return request.status_code

    def get_current_user_id(self) -> int:
        request = self.session.get(url='https://target-sandbox.my.com/api/v3/statistics/campaigns/day.json',
                                   cookies=self.cookies, params=f'date_from={date.today()}&limit=1')

        return json.loads(request.content)['items'][0]['user_id']

    def get_package_id(self, objective) -> list[int]:
        current_user_id = self.get_current_user_id()

        request = self.session.get(url='https://target-sandbox.my.com/api/v2/packages.json', cookies=self.cookies,
                                   params=f'user_id={current_user_id}')

        return [i['id'] for i in json.loads(request.content)['items'] if
                i['objective'] == [f'{objective}'] and len(i['flags']) == 1]

    def get_id_of_link(self, link) -> int:
        request = self.session.get(url='https://target-sandbox.my.com/api/v1/urls/', cookies=self.cookies,
                                   params=f'url={link}')

        return json.loads(request.content)['id']
