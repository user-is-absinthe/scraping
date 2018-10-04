from requests import get


proxy_path = 'proxy_list.txt'
all_proxy = open(proxy_path, 'r')


user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')


count_of_proxy = 100
print('Check {} proxy-servers:'.format(count_of_proxy))
good_proxy = []
counter = 0

for this_proxy in all_proxy:
    this_proxy = this_proxy.replace('\n', '')
    print('Check {} proxy.'.format(this_proxy))
    try:
        get(
            url='http://ya.ru',
            proxies={'http': this_proxy}
        )
    except IOError:
        print('    Connection error!')
    else:
        print('    All was fine.')
        good_proxy.append(this_proxy)

# while len(good_proxy) != count_of_proxy:
#     print('    Check {} proxy.'.format(all_proxy[counter]))
#     try:
#         get(
#             'http://ya.ru',
#             proxies={'http': all_proxy[counter]}
#         )
#     except IOError:
#         print('    Connection error!')
#     else:
#         print('    All was fine.')
#         good_proxy.append(all_proxy[counter])

