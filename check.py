#!/opt/python/python-3.9.0/bin/python

import subprocess
import datetime
import sys


#1. Получение данных.

#Хранилище данных из лога Nginx.
#Единый объект с доступными логами, а также промежуточными результатами работы скрипта.
obj = {
	"logs": {
		0: "/var/log/nginx/access.log",
                1: "/var/log/nginx/access.log.1.gz",
                2: "/var/log/nginx/access.log.2.gz",
                3: "/var/log/nginx/access.log.3.gz",
                4: "/var/log/nginx/access.log.4.gz",
                5: "/var/log/nginx/access.log.5.gz",
                6: "/var/log/nginx/access.log.6.gz",
                7: "/var/log/nginx/access.log.7.gz",
	},

	"result_log": {},

	"args": {},

	"duplicate": {},
	
	"count": 1
		
}

#Массив IP-адресов для подсчета количества дубликатов в логе.
ips = []


#Функции:
#Получение аргументов командной строки
def help(arr):
	error = f"""
How to use:
{arr[0]} 01/Jan/1970 site.ru
"""

	if len(arr) <= 2:
		print(error)
		sys.exit()

	if len(arr) == 3:
		result_arg = sorted(arr[1:])
		obj["args"]["date"], obj["args"]["domain"] = result_arg

	if len(arr) > 3:
		print(error)
		sys.exit()		
#Лог.
def output_log(item):
	for line in item.split('\n'):
		if line:
			new_arr = line.split()
			obj["result_log"][new_arr[0]] = (new_arr[5], new_arr[7], new_arr[14:])
			ips.append(new_arr[0])
#User-Agent из лога
def user_agent(key):
	return ''.join(obj["result_log"][key][2])
	
#URL-адрес из лога
def url(key):	
	return "".join(obj["result_log"][key][:2])
	
#Количество запросов.
def count_ip(key):
	return obj["duplicate"][key]

#Подсчет дубликатов.
def duplicate_ip(arr):
	for item in arr:
		if item in obj["duplicate"]:
			obj["duplicate"][item] += 1
		else:
			obj["duplicate"][item] = 1


help(sys.argv)

#Разница количества дней для открытия лога
check_log = int(datetime.datetime.now().strftime('%d')) - int(obj["args"]["date"].split('/')[0])

#2. Вычисления.
#Открытие лога.
try:

	nginx_log = subprocess.Popen(["sudo", "zcat", "-f", obj["logs"][check_log], obj["logs"][check_log + 1]],  stdout=subprocess.PIPE, text=True)
	grep_process = subprocess.Popen(["grep", obj["args"]["domain"]], stdin=nginx_log.stdout, stdout=subprocess.PIPE, text=True)
	output, error = grep_process.communicate()

	output_log(output)
except:
	print("Некорректные данные")


#Подсчет количества пвторяющихся элементов в словаре obj.
duplicate_ip(ips)

#Сортировка словаря от наибольшего к наименьшему.
sorted = dict(sorted(obj["duplicate"].items(), key=lambda item: item[1], reverse=True))


#3. Вывод результата
#Получение данных из словаря и отображение в терминале.

for key, value in sorted.items():

	print(f"""
------------------------------------
{obj["count"]}. [Вывод лога за дату {obj["args"]["date"]}]:

Количество запросов: [{count_ip(key)}]
IP-адрес: [{key}]

Обращение IP-адреса {key} к URL-адресу: [{url(key)}]

User-Agent IP-адреса:
[{user_agent(key)}]
------------------------------------
""", end=''
)
	obj["count"] += 1
	if obj["count"] == 6:
		break

