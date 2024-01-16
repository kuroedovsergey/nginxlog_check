# nginxlog_check
Две версии скрипта для парсинга лога веб-сервера Nginx. 

## check.sh
Входные параметры скрипта: домен и дата лога.

Скрипт проходил по всем логам в директории `/var/log/nginx`, получая информацию о количество запросов, поступивших к веб-серверу для домена за указанную дату.
Результат работы скрипта: 
```
help:
./check.sh
How to use:
./check.sh --ddos --domain site.ru - получить информацию о сайте в журнале /var/log/ddos_detect
./check.sh --ddos --iptables site.ru - получить информацию о блокировке сайта в Iptables
./check.sh --nginx --date 01/Jan/1970 --domain site.ru - получить информацию о количестве и URL-запросах к сайту

Количество запросов к сайту heartinmotion.ru за 16/Jan/2024:
    240 123.123.123.123
    231 111.111.111.111


Запросы к сайту site.ru
IP-адрес: 123.123.123.123
      1 /wp-cron.php?doing_wp_cron=1705353865.4315810203552246093750 "-" "WordPress/6.4.2; https://site.ru" "-" 0.990-0.990
      1 /wp-cron.php?doing_wp_cron=1705353565.5546030998229980468750 "-" "WordPress/6.4.2; https://site.ru" "-" 0.987-0.987


Запросы к сайту site.ru
IP-адрес: 111.111.111.111
    231 / "-" "jetmon/1.0 (Jetpack Site Uptime Monitor by
```

## check.py
Входные параметры скрипта: домен и дата лога. 

Скрипт вычисляет разницу в днях, после чего открывает необходмые логи.
Результат работы:
```
check site.ru 16/Jan/2024

------------------------------------
1. [Вывод лога за дату 16/Jan/2024]:

Количество запросов: [512]
IP-адрес: [123.123.123.123]

Обращение IP-адреса 123.123.123.123 к URL-адресу: [site.ru/wp-cron.php?doing_wp_cron=1705358665.5942130088806152343750]

User-Agent IP-адреса:
["-"0.987-0.986]
------------------------------------

------------------------------------
2. [Вывод лога за дату 16/Jan/2024]:

Количество запросов: [499]
IP-адрес: [111.111.111.111]

Обращение IP-адреса 192.0.101.226 к URL-адресу: [site.ru/]

User-Agent IP-адреса:
[SiteUptimeMonitorbyWordPress.com)""-"1.243-1.243]

```
## Деплой
Загрузка скрипта на сервер: 
```
for server in server1 server2 server3; do for num in {1..260}; do echo "Сервер $server$num:"; scp ./check.py $USER@$server$num:/home/$USER/ 2> /dev/null && ssh $server$num "chmod +x /home/$USER/check.py" 2> /dev/null && ssh $server$num "echo \"alias check='python3 /home/$USER/check.py'\" >> /home/$USER/.bashrc" 2> /dev/null; done done
```
