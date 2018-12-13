import random
from datetime import datetime
import multiprocessing

import my_csv

import requests
import fake_useragent


PATH_TO_LINKS = 'C:\\Users\Worker\Pycharm\Pycharm_project\scraping\\beboo\partly\data\photos_links_30k.csv'
PATH_TO_PROXIES = 'C:\\Users\Worker\Pycharm\Pycharm_project\scraping\\beboo\partly\data\proxies_good.txt'
PATH_TO_PHOTOS = 'data/photos'

DEFAULT_TIMEOUT = 5
# DEFAULT_THREADS = 100
DEFAULT_THREADS = 5  # for test

LOCK = multiprocessing.Lock()
PROXIES_LIST = list()


def open_links(path):
    all_data = my_csv.csv_reader(path, separator='\t', headline=False, encode='utf-8')
    ids_list_f = all_data[0]
    numbers_list_f = all_data[1]
    links_list_f = all_data[2]
    return ids_list_f, numbers_list_f, links_list_f


def load_proxies(input_file=PATH_TO_PROXIES):
    with open(input_file, "r") as Fi:
        proxies = set(Fi.readlines())
    proxies = list(proxies)
    proxies = [this.strip() for this in proxies]
    return proxies


def save_photo(id_user, id_photo, photo_link, proxie_list, timeout):
    global PATH_TO_PHOTOS
    photo_big_link = photo_link.replace('800x800', '1200x1200')
    to_save = get_photo(photo_big_link, proxie_list, timeout)
    if to_save == 400:
        to_save = get_photo(photo_link, proxie_list, timeout)
    elif to_save == 400:
        return 1
    file_name = PATH_TO_PHOTOS + id_user + '_' + id_photo + '.jpg'
    with open(file_name, 'wb') as out:
        out.write(to_save.content)
    my_print('Save photo {} from {} user.'.format(id_photo + 1, id_user))
    return 0


def get_photo(link, proxie_list, timeout):
    # global PROXIES_LIST, DEFAULT_TIMEOUT
    user_agent = fake_useragent.UserAgent().random
    LOCK.acquire()
    try:
        proxy = {'https': random.choice(proxie_list)}
    finally:
        LOCK.release()
    content = None
    try:
        content = requests.get(
            url=link,
            headers=user_agent,
            proxies=proxy,
            # timeout=timeout
        )
    except requests.exceptions.Timeout:
        index = proxie_list.index(proxy['https'])
        proxie_list.pop(index)
        get_photo(link)

    if content.status_code != 200:
        return 400
    return content


def my_print(line=''):
    to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t'
    print(to_write + str(line))


def main():
    my_print('Start program.')
    global PROXIES_LIST, PATH_TO_LINKS, DEFAULT_THREADS, DEFAULT_TIMEOUT
    PROXIES_LIST = load_proxies(PATH_TO_PROXIES)
    ids_list, numbers_list, links_list = open_links(PATH_TO_LINKS)
    # lock = multiprocessing.Lock()
    # pool = multiprocessing.Pool(DEFAULT_THREADS)
    # pool = multiprocessing.Pool
    # for link in all_links_list:
    #     pool.apply_async(func=save_photo, args=(link[0], link[1], link[2]))
    # pool.close()
    # pool.join()

    # for link in all_links_list:
    #     pool.apply_async(func=save_photo, args=(link[0], link[1], link[2]))
    # pool.close()
    # pool.join()

    # with pool(DEFAULT_THREADS) as p:
    #     for index in range(len(ids_list)):
    #         p.apply_async(func=save_photo, args=(ids_list[index], numbers_list[index], links_list[index]))

    all_pr = list()
    for index in range(len(ids_list)):
        pr = multiprocessing.Process(
            target=save_photo,
            args=(ids_list[index], numbers_list[index], links_list[index], PROXIES_LIST, DEFAULT_TIMEOUT)
        )
        all_pr.append(pr)
        pr.start()
    for pr in all_pr:
        pr.join()

    pass


if __name__ == '__main__':
    main()
    # print(open_links(PATH_TO_LINKS))
