import csv
import random
import requests
import fake_useragent

PATH_TO_PHOTOS = 'data/photos/'
PATH_TO_PHOTOS_LINKS = 'data/'
PATH_TO_PROXIES = '/Users/owl/Pycharm/PycharmProjects/scraping/beboo/partly/data/proxies_good.txt'


PROXIES_LIST = list()


def main():
    global PROXIES_LIST
    PROXIES_LIST = load_proxies()
    data = load_links('/Users/owl/Pycharm/PycharmProjects/scraping/beboo/partly/data/test_photos_links_all.csv')
    for number, photo in enumerate(data):
        print('Work with {}/{} ({}% done) photo.'.format(
            number,
            len(data),
            number/len(data)*100
        ))
        save_photo(photo[0], photo[1], photo[2])


def load_proxies(input_file=PATH_TO_PROXIES):
    with open(input_file, "r") as Fi:
        proxies = set(Fi.readlines())
    proxies = list(proxies)
    proxies = [this.strip() for this in proxies]
    return proxies


def load_links(path_to_photos):
    with open(path_to_photos, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()
    file_lines = [line.split('\t') for line in file_lines]
    return file_lines


def write_csv(path, data):
    with open(path, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for line in data:
            writer.writerow(line)
    # print('CSV in {} created successful!'.format(path))
    pass


def save_photo(user_id, photo_id, photo_link):
    global PATH_TO_PHOTOS, PATH_TO_PHOTOS_LINKS, PROXIES_LIST
    photo_link = photo_link.replace('\n', '')
    photo_big_link = photo_link.replace('800x800', '1200x1200')
    user_agent = fake_useragent.UserAgent().random
    proxy = {'https': random.choice(PROXIES_LIST)}
    try:
        to_save = requests.get(
            url=photo_big_link,
            headers=user_agent,
            proxies=proxy
        )
        if to_save.status_code == 404:
            to_save = requests.get(
                url=photo_link,
                headers=user_agent,
                proxies=proxy
            )
    except requests.ConnectionError or requests.Timeout or requests.ConnectTimeout:
        print('\tPassed.')
        return 1
    photo_name = PATH_TO_PHOTOS + '{}_{}.jpg'.format(user_id, photo_id)  # user_id + photo number
    out = open(photo_name, "wb")
    out.write(to_save.content)
    out.close()
    write_csv(PATH_TO_PHOTOS_LINKS, [[user_id, photo_id, photo_link]])
    print('\tSaved.')
    return 0


if __name__ == '__main__':
    main()
