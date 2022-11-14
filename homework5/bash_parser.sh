#!/bin/bash
exec 1>result_bash.txt
echo -e 'Общее количество запросов:'
cat access.log | wc -l 
GET=$(grep "\"GET " access.log| wc -l)
POST=$(grep "\"POST " access.log| wc -l)
HEAD=$(grep "\"HEAD " access.log| wc -l)
PUT=$(grep "\"PUT " access.log | wc -l)
other=$(egrep "\"PUT |\"POST |\"GET |\"HEAD " -v access.log | wc -l)
echo -e '\nОбщее количество GET, POST, HEAD, PUT запросов:'
echo GET-$GET, POST-$POST, HEAD-$HEAD, PUT-$PUT, other-$other 
echo -e '\nТоп 10 самых частых запросов:'
awk '{print $7}' access.log | sort | uniq -c | sort -r | head | awk 'BEGIN {print "URL Requests-count"} {print $2, $1}' | column -t
echo -e '\nТоп 5 самых больших по размеру запросов, которые завершились клиентской 4ХХ ошибкой:'
awk '$9 ~ /4[[:digit:]]{2}/' access.log | awk '{print $7,$9,$10,$1}' | sort -k 3 -nr | uniq | head -n 5 | awk 'BEGIN {print "URL Status-code Request-size IP"} {print $0}' | column -t 
echo -e '\nТоп 5 пользователей по количеству запросов, которые завершились серверной 5ХХ ошибкой:'
awk '$9 ~ /5[[:digit:]]{2}/' access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 5 | awk 'BEGIN {print "IP Requests-count"} {print $2, $1}' | column -t
