import re
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

with open('access.log') as logfile:
    lines = logfile.readlines()


def count_lines_matches_with_string(string):
    res = []
    for i in lines:
        search_result = re.search(string, i)
        if search_result is not None:
            res.append(i)

    return len(res)


def get_lines_matches_with_string_in_field(string, field_number):
    res = []
    for i in lines:
        required_field = i.split()[field_number]
        search_result = re.search(string, required_field)
        if search_result is not None:
            res.append(i)

    return res


def count_lines_with_same_field(field_number: int, data: list):
    res = {}
    for i in data:
        required_field = i.split()[field_number]
        if required_field not in res:
            res[required_field] = 1
        else:
            res[required_field] += 1

    return res


def sort_dictionary_by_value(dictionary):
    sorted_dictionary = {}
    sorted_keys = sorted(dictionary, key=dictionary.get, reverse=True)
    for i in sorted_keys:
        sorted_dictionary[i] = dictionary[i]

    return sorted_dictionary


def make_dictionary_with_required_field(l: list, field_number):
    dictionary = {}
    for i in l:
        dictionary[i] = int(i.split()[field_number])

    return dictionary


def dictionary_with_unique_uri(dictionary):
    unique_dictionary = {}
    for key in dictionary.keys():
        if key.split()[6] not in unique_dictionary.keys():
            unique_dictionary[key] = dictionary[key]

    return unique_dictionary


def get_first_dictionary_lines(dictionary, lines_amount=10):
    dictionary_head = {}
    items = list(dictionary.items())
    for i in range(lines_amount):
        dictionary_head[items[i][0]] = items[i][1]

    return dictionary_head


requests_amount = len(lines)
get_requests_amount = count_lines_matches_with_string('"GET ')
head_requests_amount = count_lines_matches_with_string('"HEAD ')
post_requests_amount = count_lines_matches_with_string('"POST ')
put_requests_amount = count_lines_matches_with_string('"PUT ')
other_requests_amount = requests_amount - get_requests_amount \
                        - head_requests_amount - post_requests_amount - put_requests_amount

ten_frequent_requests = get_first_dictionary_lines(
    sort_dictionary_by_value(count_lines_with_same_field(6, lines)))

status_5xx = get_lines_matches_with_string_in_field('5\d\d', 8)
status_4xx = get_lines_matches_with_string_in_field('4\d\d', 8)

five_highest_request_with_4XX_code = get_first_dictionary_lines(
    dictionary_with_unique_uri(sort_dictionary_by_value(
        make_dictionary_with_required_field(status_4xx, 9))), 5)

five_highest_request_with_4XX_code_dict = {}
for k, v in five_highest_request_with_4XX_code.items():
    k = k.split()
    five_highest_request_with_4XX_code_dict[f'{k[6]} {k[8]}'] = f'{k[9]} {k[0]}'

five_frequent_users_with_5XX_code_dict = get_first_dictionary_lines(
    sort_dictionary_by_value(count_lines_with_same_field(0, status_5xx)), 5)

if args.json:
    result = {'Total requests': requests_amount,
              'Total requests by type': f'GET-{get_requests_amount}, POST-{post_requests_amount}, '
                                        f'HEAD-{head_requests_amount}, PUT-{put_requests_amount}, '
                                        f'other-{other_requests_amount}',
              'Top 10 most frequent requests': ten_frequent_requests,
              'Top 5 biggest request with 4XX code': five_highest_request_with_4XX_code_dict,
              'Top 5 users by requests amount with 5XX code': five_frequent_users_with_5XX_code_dict
              }
    with open('result_python.json', 'w') as file:
        json.dump(result, file)
else:
    with open('result_python.txt', 'w') as file:
        file.write((f'Общее количество запросов:\n'
                    f'{requests_amount}\n'
                    f'\nОбщее количество запросов по типу:\n'
                    f'GET-{get_requests_amount}, POST-{post_requests_amount}, '
                    f'HEAD-{head_requests_amount}, PUT-{put_requests_amount}, other-{other_requests_amount}\n'
                    f'\nТоп 10 самых частых запросов:\n'))

        for k, v in ten_frequent_requests.items():
            file.write(f'{k} {str(v)}\n')

        file.write('\nТоп 5 самых больших по размеру запросов, которые завершились клиентской 4ХХ ошибкой:\n')
        for k, v in five_highest_request_with_4XX_code_dict.items():
            file.write(f'{k} {v}\n')

        file.write('\nТоп 5 пользователей по количеству запросов, которые завершились серверной 5ХХ ошибкой:\n')
        for k, v in five_frequent_users_with_5XX_code_dict.items():
            file.write(f'{k} {v}\n')
