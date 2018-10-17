rem таймауты увеличены
python proxy_checker.py -i proxies.txt -r 1 -t 10000 -k 0 -p 150
rem python proxy_checker.py -i proxies_good.txt -r 4 -t 5000 -k 2 -p 150
rem python proxy_checker.py -i proxies_good.txt -r 1 -k 1 -g -t 10000 -p 100
rem обработка хороших - отдельно - good