from os import makedirs, path
from time import sleep
from random import randint

from requests import get, codes


def img_saver(url, counter, now_proxy, directory, is_png):
    if not path.exists(directory):
        makedirs(directory)

    name = directory + '/' + str(counter) + '.jpg'
    if is_png:
        name = name.replace('.jpg', '.png')

    if now_proxy == 0:
        r = get(url)
    else:
        print('Now use {} proxy.'.format(now_proxy))
        in_proxy = {"http": now_proxy}
        r = get(url, proxies=in_proxy)

    if r.status_code == codes.ok:
        out = open(name, "wb")
        out.write(r.content)
        out.close()
    else:
        # print('All.')
        return 1

    print('\t{} images saved successfully.'.format(counter))
    return 0


def load_proxies(input_file):
    with open(input_file, "r") as Fi:
        proxies = set(Fi.readlines())
    return proxies


def manga_saver(first_url, proxy_path=''):
    counter = 1
    dir_name = url_first.replace('https://i.nhentai.net/galleries/', '')
    dir_name = dir_name.replace('/1.jpg', '')
    dir_name = dir_name.replace('/1.png', '')
    if len(proxy_path) != 0:
        use_proxy = 1
    # if use_proxy == 1:
        print('Proxy mode on.')
        proxy = list(load_proxies('proxies_good.txt'))
    print('Saved in {} directory.'.format(dir_name))
    denial_of_service = 0
    max_denial_of_service = 10
    png = False
    while True:
        if use_proxy == 1:
            now_proxy = proxy[randint(0, len(proxy) - 1)].replace('\n', '')
        else:
            now_proxy = 0
        url_now = first_url.replace('/1.jpg', '/' + str(counter) + '.jpg')
        # url_now = first_url.replace('/1.png', '/' + str(counter) + '.png')
        if png:
            url_now = url_now.replace('.jpg', '.png')
        if img_saver(url_now, counter, now_proxy, dir_name, png) == 1:
            denial_of_service += 1
            png = not png
            if denial_of_service == max_denial_of_service:
                print('That`s all.')
                break
            else:
                counter -= 1
        if use_proxy == 0:
            sleep(1)
        counter += 1


if __name__ == '__main__':
    url_first = 'https://i.nhentai.net/galleries/0000/1.jpg'
    path_to_proxy = 'proxies_good.txt'
    # use_proxy = 1
    manga_saver(url_first, path_to_proxy)
