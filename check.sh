#!/bin/bash

ME0=$0

function help {
  echo "How to use:"
  echo "$ME0 --ddos --domain site.ru - получить информацию о сайте в журнале /var/log/ddos_detect"
  echo "$ME0 --ddos --iptables site.ru - получить информацию о блокировке сайта в Iptables"
  echo "$ME0 --nginx --date 01/Jan/1970 --domain site.ru - получить информацию о количестве и URL-запросах к сайту" 
}


trap "exit" SIGHUP SIGINT SIGTERM

function nginxlog {
	echo Количество запросов к сайту $2 за $1:; sudo ls /var/log/nginx | grep access* | while read log; do sudo zcat -f /var/log/nginx/$log | grep -i $1 \
	| grep $2; done  | cut -f 1 -d ' ' -s | sort -n | uniq -c | sort -rn | head -20; echo && sudo ls /var/log/nginx | grep access* | while read log; \
	do sudo zcat -f /var/log/nginx/$log | grep -i $1 | grep $2; done | cut -f 1 -d ' ' -s | sort -n | uniq -c | sort -rn | head -5 | \
	grep -E -o '([0-9]{1,3}[\.]){3}[0-9]{1,3}' > /home/$USER/ipstat.txt && cat ipstat.txt | while read ip; do echo "Запросы к сайту $2"; echo "IP-адрес: $ip";\
	 sudo ls /var/log/nginx | grep access* | while read log; do sudo zcat -f /var/log/nginx/$log | grep -i $1 | grep $2 | grep $ip; done | cut -f 8,12-18 -d ' ' -s \
	| sort -n | uniq -c | sort -rn | tail -5; echo; done && rm /home/$USER/ipstat.txt

}


function checkipstat {
	if [ -f ~/ipstat.txt ]
	then
		rm ~/ipstat.txt
		nginxlog $1 $2
	else
		nginxlog $1 $2
	fi
}


function iptablesddos {
		echo "Проверка блокировки домена сервисом Iptables:"
		sudo /sbin/iptables -Z BAN && sudo /sbin/iptables -L -nv| grep $1 ; sleep 60 ; sudo /sbin/iptables -L -nv | grep $1
}


if [ $# = 0 ]; then
    help
fi

while [[ "$#" -gt 0 ]]
  do
    case $1 in
      --ddos)
      		while [[ "$#" -gt 0 ]]
				do
				    case $1 in
				      --domain) DomainDDoS="$2"; shift;
				      			   ddos $DomainDDoS;;

				      --iptables) Domain="$2"; shift;
				      			   iptablesddos $Domain;;  	 
				    esac
				    shift
				done
		;;
      --nginx)
      		trigger="start"
      		while [[ "$#" -gt 0 ]]
				do
				    case $1 in
				      --date) Nginxdate="$2"; shift;;

				      --domain) Nginxdomain="$2"; shift;; 
				    esac
				    shift
				done
		;;
		?) echo "Неправильный параметр"
           echo "Для вывода справки запустите скрипт без параметров."
           exit 1
           ;;
        :) echo "Не задан дополнительный аргумент"
           echo "Запустите скрипт без параметров, чтобы узнать какой дополнительный параметр можно подставить."
           ;;
    esac
    shift
done


if [ "$trigger" = "start" ]; then
	checkipstat $Nginxdate $Nginxdomain
fi
