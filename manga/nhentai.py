from os import makedirs, path
from time import sleep

from urllib.request import urlretrieve, ProxyHandler, build_opener, install_opener
from urllib.error import HTTPError


def img_saver(url):
    directory = 'save_pic'
    if not path.exists(directory):
        makedirs(directory)
    name = directory + '/' + url.replace('/', '') + '.jpg'
    try:
        urlretrieve(url, name)
    except HTTPError:
        return 1
    print('Images saved successfully.')
    return 0


def load_proxies(input_file):
    with open(input_file, "r") as Fi:
        proxies = set(Fi.readlines())
    return proxies


if __name__ == '__main__':
    url_first = '1'
    counter = 1
    # set_proxies = load_proxies(input_file='proxies_good.txt')
    proxy = ProxyHandler({'http': '167.249.248.122:33865'})
    opener = build_opener(proxy)
    install_opener(opener)
    while True:
        url_now = url_first.replace('/1.jpg', '/' + str(counter) + '.jpg')
        if img_saver(url_first) == 1:
            break
        sleep(3)
        counter += 1
