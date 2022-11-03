# Скрипты для анализа логов nginx (access.log) на **Python** и **Bash**


## Bash скрипт - *bash_parser.sh*

```exec 1>result_bash.txt``` - перенаправляет STDOUT в файл **result_bash.txt**
##### Общее количество запросов
Выводит общее количество запросов путем подсчета количества строк :
```
 cat access.log | wc -l 
```
##### Общее количество GET, POST, HEAD, PUT запросов 

Заводит переменные, хранящие количество запросов каждого типа :
( Грепаем строки с нужной подстрокой из файла и считаем их количество )
```
GET=$(grep "\"GET " access.log| wc -l)
POST=$(grep "\"POST " access.log| wc -l)
HEAD=$(grep "\"HEAD " access.log| wc -l)
PUT=$(grep "\"PUT " access.log | wc -l)
other=$(egrep "\"PUT |\"POST |\"GET |\"HEAD " -v access.log | wc -l)
```
Выводит переменные, хранящие количество запросов по типам :
```
echo GET-$GET, POST-$POST, HEAD-$HEAD, PUT-$PUT, other-$other 
```
##### Топ 10 самых частых запросов
( Берем 7-ую колонку - урлы запросов файла access.log -> сортируем для следующей операции, так как uniq видит строчки, находящиеся рядом -> применяем uniq с флагом -c для подсчета количества повторений урлов -> сортируем по возрастанию -> берем первые 10 строк -> передаем вывод на оформление )
```
awk '{print $7}' access.log | sort | uniq -c | sort -r | head | awk 'BEGIN {print "URL Requests-count"} {print $2, $1}' | column -t
```
##### Топ 5 самых больших по размеру запросов, которые завершились клиентской 4xx ошибкой
( Отбираем строки из файла access.log по 9 колонке, имеющих совпадения с регулярным выражением ```4[[:digit:]]{2}``` ->  выводим нужные строки -> сортируем по 3-му столбцу с флагом -nr, то есть по значению байтового размера запроса по убыванию  -> исключаем одинаковые строки -> берем первые 5 строк -> передаем вывод на оформление )
```
awk '$9 ~ /4[[:digit:]]{2}/' access.log | awk '{print $7,$9,$10,$1}' | sort -k 3 -nr | uniq | head -n 5 | awk 'BEGIN {print "URL Status-code Request-size IP"} {print $0}' | column -t 
```
##### Топ 5 пользователей по количеству запросов, которые завершились серверной 5xx ошибкой
( Отбираем строки из файла access.log по 9 колонке, имеющих совпадения с регулярным выражением ```5[[:digit:]]{2}``` -> выводим 1 строку, то есть IP пользователя -> сортируем для корректной работы команды uniq -> исключаем одинаковые строки и считаем количество их повторений -> сортируем по убыванию количества запросов -> берем первые 5 строк -> передаем вывод на оформление )
```
awk '$9 ~ /5[[:digit:]]{2}/' access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 5 | awk 'BEGIN {print "IP Requests-count"} {print $2, $1}' | column -t 
```
## Python скрипт -  *python_parser.py*
```import re``` - импорт библиотеки, имеющей методы поиска по регулярным выражениям
```import argparse``` - импорт парсера флагов для запуска скрипта
```import json``` - импорт модуля для кодировки формата JSON
##### Преднастройки скрипта
Парсинг флага ```--json```
```
parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
```
Чтение файла *access.log*
```
with open('access.log') as logfile:
    lines = logfile.readlines()
```
Объявление кастомных функций для обработки информации
```
count_lines_matches_with_string(string) - возвращает количество строк имеющих совпадение с string 
get_lines_matches_with_string_in_field(string, field_number) - возвращает список строк имеющих совпадение с string в поле field_number
count_lines_with_same_field(field_number, data) - возвращает словарь из названия поля под номером field_number, принимает data - список из строк
sort_dictionary_by_value(dictionary) - сортирует словарь dictionary по его value в порядке убывания
make_dictionary_with_required_field(l, field_number) - возвращает словарь, где ключи - элементы списка l, значения - определенное поле под номером field_number элемента списка l
dictionary_with_unique_uri(dictionary) - возвращает словарь, в котором отброшены повторения uri в словаре dictionary
get_first_dictionary_lines(dictionary, lines_amount=10) - полный аналог команды head в Bash. Возвращает первые lines_amount элементов из словаря dictionary, по умолчанию - 10 
```
##### Общее количество запросов
Объявляет переменную, которая хранит количество запросов ( то есть длину полученного списка при прочтение файла *access.log* )
```
requests_amount = len(lines)
```
##### Общее количество GET, POST, HEAD, PUT запросов
Объявляет переменные, которые хранят количетво запросов по каждому типу, используя регулярные выражения, передаваемые функции ```count_lines_matches_with_string```
```
get_requests_amount = count_lines_matches_with_string('"GET ')
head_requests_amount = count_lines_matches_with_string('"HEAD ')
post_requests_amount = count_lines_matches_with_string('"POST ')
put_requests_amount = count_lines_matches_with_string('"PUT ')
other_requests_amount = requests_amount - get_requests_amount \
                        - head_requests_amount - post_requests_amount - put_requests_amount
```
##### Топ 10 самых частых запросов
Объявляет переменную, хранящую 10 самых частых запросов
( Считаем количество строк с одинаковым полем uri -> сортируем полученный список по убыванию значений -> берем первые 10 строк из отсортированного списка )
```
ten_frequent_requests = get_first_dictionary_lines(
    sort_dictionary_by_value(count_lines_with_same_field(6, lines)))
```
``status_5xx = get_lines_matches_with_string_in_field('5\d\d', 8)`` - список строк, имеющих код 5хх  
``status_4xx = get_lines_matches_with_string_in_field('4\d\d', 8)`` - список строк, имеющих код 4хх

##### Топ 5 самых больших по размеру запросов, которые завершились клиентской 4xx ошибкой
( Форматируем полученный ранее список в словарь, с ключами - элементами списка, значениями - байтовыми размерами запроса -> сортируем по убыванию размера запроса -> убираем повторяющиеся uri -> берем первые 5 элементов словаря. Далее в цикле обрабатываем словарь для красивого вывода )
```
five_highest_request_with_4XX_code = get_first_dictionary_lines(
    dictionary_with_unique_uri(sort_dictionary_by_value(
        make_dictionary_with_required_field(status_4xx, 9))), 5)
five_highest_request_with_4XX_code_dict = {}
for k, v in five_highest_request_with_4XX_code.items():
    k = k.split()
    five_highest_request_with_4XX_code_dict[f'{k[6]} {k[8]}'] = f'{k[9]} {k[0]}'
```
##### Топ 5 пользователей по количеству запросов, которые завершились серверной 5xx ошибкой
( Считаем ранее полученный список, состоящий из строк с ошибкой 5хх, получая словарь запрос-количество повторений -> сортируем словарь по убыванию значения -> отбираем первые 5 элементов )
```
five_frequent_users_with_5XX_code_dict = get_first_dictionary_lines(
    sort_dictionary_by_value(count_lines_with_same_field(0, status_5xx)), 5)
```
##### Запись полученной информации в файлы **result_python.txt** и **result_python.json**
Если Python скрипт запущен с флагом ```--json```, то создается словарь ``result``, который содержит информацию для дальнейшей записи в файл **result_python.json**
```
if args.json:
    result = {'Total requests': requests_amount,
              'Total requests by type': f'GET-{get_requests_amount}, POST-{post_requests_amount}, '
                                        f'HEAD-{head_requests_amount}, PUT-{put_requests_amount}, '
                                        f'other-{other_requests_amount}',
              'Top 10 most frequent requests': ten_frequent_requests,
              'Top 5 biggest request with 4XX code': five_highest_request_with_4XX_code_dict,
              'Top 5 users by requests amount with 5XX code': five_frequent_users_with_5XX_code_dict
              }
```
```json.dump``` форматирует словарь result и записывает его в файл
```
    with open('result_python.json', 'w') as file:
        json.dump(result, file)
```
Иначе скрипт поочередно запишет всю информацию в файл **result_python.txt**
```
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
```