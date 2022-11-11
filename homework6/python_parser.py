import re
import os


class ParsedLogs:
    def __init__(self):
        self.lines = None
        with open(os.path.join(os.path.abspath(os.path.join(__file__, os.path.pardir)), 'accesslogs.txt')) as logfile:
            self.lines = logfile.readlines()

    def count_lines_matches_with_string(self, string):
        res = []
        for i in self.lines:
            search_result = re.search(string, i)
            if search_result is not None:
                res.append(i)

        return len(res)

    def get_lines_matches_with_string_in_field(self, string, field_number):
        res = []
        for i in self.lines:
            required_field = i.split()[field_number]
            search_result = re.search(string, required_field)
            if search_result is not None:
                res.append(i)

        return res

    @staticmethod
    def count_lines_with_same_field(field_number: int, data: list):
        res = {}
        for i in data:
            required_field = i.split()[field_number]
            if required_field not in res:
                res[required_field] = 1
            else:
                res[required_field] += 1

        return res

    @staticmethod
    def sort_dictionary_by_value(dictionary):
        sorted_dictionary = {}
        sorted_keys = sorted(dictionary, key=dictionary.get, reverse=True)
        for i in sorted_keys:
            sorted_dictionary[i] = dictionary[i]

        return sorted_dictionary

    @staticmethod
    def make_dictionary_with_required_field(l: list, field_number):
        dictionary = {}
        for i in l:
            dictionary[i] = int(i.split()[field_number])

        return dictionary

    @staticmethod
    def dictionary_with_unique_uri(dictionary):
        unique_dictionary = {}
        for key in dictionary.keys():
            if key.split()[6] not in unique_dictionary.keys():
                unique_dictionary[key] = dictionary[key]

        return unique_dictionary

    def get_info(self):
        requests_amount = len(self.lines)
        get_requests_amount = self.count_lines_matches_with_string('"GET ')
        head_requests_amount = self.count_lines_matches_with_string('"HEAD ')
        post_requests_amount = self.count_lines_matches_with_string('"POST ')
        put_requests_amount = self.count_lines_matches_with_string('"PUT ')
        other_requests_amount = requests_amount - get_requests_amount - \
                                head_requests_amount - post_requests_amount - put_requests_amount

        most_frequent_requests = self.sort_dictionary_by_value(self.count_lines_with_same_field(6, self.lines))

        status_5xx = self.get_lines_matches_with_string_in_field('5\d\d', 8)
        status_4xx = self.get_lines_matches_with_string_in_field('4\d\d', 8)

        highest_request_with_4XX_code = self.dictionary_with_unique_uri(
            self.sort_dictionary_by_value(self.make_dictionary_with_required_field(status_4xx, 9)))

        highest_request_with_4XX_code_dict = {}
        for k, v in highest_request_with_4XX_code.items():
            k = k.split()
            highest_request_with_4XX_code_dict[f'{k[6]} {k[8]}'] = f'{k[9]} {k[0]}'

        frequent_users_with_5XX_code_dict = self.sort_dictionary_by_value(
            self.count_lines_with_same_field(0, status_5xx))

        return {'requests_amount': requests_amount,
                'get_requests_amount': get_requests_amount,
                'head_requests_amount': head_requests_amount,
                'post_requests_amount': post_requests_amount,
                'put_requests_amount': put_requests_amount,
                'other_requests_amount': other_requests_amount,
                'most_frequent_requests': most_frequent_requests,
                'five_highest_request_with_4XX_code_dict': highest_request_with_4XX_code_dict,
                'five_frequent_users_with_5XX_code_dict': frequent_users_with_5XX_code_dict
                }
