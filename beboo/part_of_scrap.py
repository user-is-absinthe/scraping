import multiprocessing
from datetime import datetime

import my_csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as selenium_exception

COUNT_OF_BROWSER = 20

PATH_TO_LOG = 'data/new_users.log'
# PATH_TO_USERS_LINKS = 'data/users_links.csv'
PATH_TO_USERS_LINKS = 'data/users_links_100.csv'
PATH_TO_USERS_INFORMATION = 'data/new_users.csv'
PATH_TO_PHOTOS_LINKS = 'data/photos_links.csv'
# PATH_TO_PHOTOS = 'data/photos'

PATH_TO_WEBDRIVER = 'C:\\Users\Worker\Pycharm\Pycharm_project\scraping\\beboo\chromedriver'

GRAY_USERS = 0
WHITE_USERS = 0
BLACK_USERS = 0


# def csv_reader(path, separator, headline=False, encode='utf-16'):
#     with open(path, 'r', encoding=encode) as file:
#         csv_file = file.readlines()
#     csv_file = [this.strip() for this in csv_file]
#     if headline:
#         keys_to_dict = csv_file[0].split(separator)
#     else:
#         keys_to_dict = [i for i in range(0, len(csv_file[0].split(separator)))]
#
#     opened_csv = dict()
#     for key in keys_to_dict:
#         opened_csv[key] = list()
#
#     for line in csv_file:
#         if headline and line == csv_file[0]:
#             continue
#         separated_line = line.split(separator)
#         for index in range(len(keys_to_dict)):
#             opened_csv[keys_to_dict[index]].append(separated_line[index])
#
#     return opened_csv
#
#
# def csv_line_writer(path, data, separator='\t', encode='utf-16'):
#     csv_file = open(path, 'a', encoding=encode)
#     line = ''
#     for column in data:
#         line += str(column)
#         if column != data[-1]:
#             line += separator
#     line += '\n'
#     csv_file.write(line)
#     csv_file.close()


def write_csv_head():
    my_csv.csv_line_writer(PATH_TO_USERS_INFORMATION,
                           [
                               'id_user', 'link_to_user', 'имя', 'пол', 'тип аккаунта', 'возраст', 'страна',
                               'город', 'о себе', 'кого ищет', 'семейное положение', 'доход', 'материальное положение',
                               'проживание', 'наличие автомобиля', 'отношение к курению', 'отношение к алкоголю',
                               'знание языков', 'рост, см', 'вес, кг', 'цвет волос', 'цвет глаз', 'телосложение',
                               'татуировки', 'пирсинг', 'волосы на лице и на теле', 'ориентация', 'тип секса', 'роль',
                               'позы', 'действия', 'эрогенные зоны', 'фетиши'
                           ]
                           )
    my_csv.csv_line_writer(PATH_TO_PHOTOS_LINKS, ['id_user', 'number_of_photo', 'link_to_photo'])
    information('CSV head created successful.')


def information(info):
    to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t' + info + '\n'
    print(to_write)
    with open(PATH_TO_LOG, 'a') as file:
        file.write(to_write)
    pass


def load_user_links():
    user_links_all = my_csv.csv_reader(path=PATH_TO_USERS_LINKS, separator='\t', headline=False, encode='utf-16')
    user_links = user_links_all[0]
    users_code = user_links_all[1]
    information('User links load successful.')
    return user_links, users_code


def auth(dr):
    dr.get('http://beboo.ru/auth')
    elem = dr.find_element_by_name('email')
    elem.send_keys("kozlovsky.andryu@ya.ru")
    elem1 = dr.find_element_by_name('password')
    elem1.send_keys("10bFYWH4p5")
    elem.send_keys(Keys.RETURN)
    return dr


def find_by(param_name, param_text, dr):
    try:
        if param_name == 'class':
            return dr.find_element_by_class_name(param_text).text
        elif param_name == 'id':
            return dr.find_element_by_id(param_text).text
        elif param_name == 'tag_1':
            return dr.find_elements_by_tag_name(param_text)[1].text.lower()
        elif param_name == 'tag_2':
            return dr.find_elements_by_tag_name(param_text)[2].text
        elif param_name == 'tag_4':
            return dr.find_elements_by_tag_name(param_text)[4].text
        elif param_name == 'tag_6':
            return dr.find_elements_by_tag_name(param_text)[6].text
        elif param_name == 'tag_7':
            return dr.find_elements_by_tag_name(param_text)[6].text
        elif param_name == 'photos':
            return dr.find_elements_by_class_name(param_text)
    except selenium_exception.NoSuchElementException:
        return 'nd'


def scr_user(dr, link_to_user, region_code):
    dr = auth(dr)
    dr.get(link_to_user)
    try:
        dr.find_element_by_class_name('info-404')
        # write_csv(path_to_users_information, [[id_user, 'User']])
    except selenium_exception.NoSuchElementException:
        id_user = link_to_user.link_to_user.replace('http://beboo.ru/profile/', '').replace('?from=1', '')
        name = find_by('class', 'profile-nick-name', dr).partition('\n')[0]
        sex = find_by('id', 'val_age', dr)
        type_of_account = find_by('tag_1', 'dd', dr)
        age = find_by('tag_2', 'dd', dr)
        country = region_code
        # country = '1'  # сделать подстановку из словаря, ищем по строке
        # driver.find_element_by_class_name('look_for').text и если совпадает со страной из списка, подставляем её
        city = find_by('tag_4', 'dd', dr)
        about = find_by('tag_6', 'p', dr)
        find = find_by('tag_7', 'p', dr)

        # about
        family = find_by('id', 'val_25', dr)  # семейное положение
        profit = find_by('id', 'val_26', dr)  # доход
        financial_situation = find_by('id', 'val_27', dr)  # материальное положение
        accommodation = find_by('id', 'val_28', dr)  # проживание
        auto = find_by('id', 'val_29', dr)  # наличие автомобиля
        smoke = find_by('id', 'val_30', dr)  # отношение к курению
        alco = find_by('id', 'val_31', dr)  # отношение к алкоголю
        language = find_by('id', 'val_32', dr)  # знание языков

        # look
        height = find_by('id', 'val_height', dr).replace(' см', '')  # рост, см
        weight = find_by('id', 'val_weight', dr).replace(' кг', '')  # вес, кг
        head_color = find_by('id', 'val_23', dr)  # цвет волос
        eye_color = find_by('id', 'val_24', dr)  # цвет глаз
        body = find_by('id', 'val_19', dr)  # телосложение
        tatoo = find_by('id', 'val_20', dr)  # татуировки
        piercing = find_by('id', 'val_21', dr)  # пирсинг !!!
        other_hair = find_by('id', 'val_22', dr)  # волосы на лице и на теле

        # sexual preferences
        orientation = find_by('id', 'val_33', dr)  # ориентация
        type_of_sex = find_by('id', 'val_35', dr)  # тип секса
        role_of_sex = find_by('id', 'val_34', dr)  # роль
        favorite_poses_in_sex = find_by('id', 'val_36', dr)  # позы
        to_do = find_by('id', 'val_37', dr)  # действия !!!
        erogenous_zones = find_by('id', 'val_38', dr)  # эрогенные зоны
        fetishes = find_by('id', 'val_39', dr)  # фетиши

        # TODO: save info
        global PATH_TO_USERS_INFORMATION
        my_csv.csv_line_writer(PATH_TO_USERS_INFORMATION, [
            id_user, link_to_user, name, sex, type_of_account, age, country, city, about, find, family, profit,
            financial_situation, accommodation, auto, smoke, alco, language, height, weight, head_color, eye_color,
            body, tatoo, piercing, other_hair, orientation, type_of_sex, role_of_sex, favorite_poses_in_sex, to_do,
            erogenous_zones, fetishes
        ])

        users_photos_links = get_links_to_photo(dr)

        # users_photos_links_to_save = []
        # for i in range(len(users_photos_links)):
        #     users_photos_links_to_save.append([id_user, users_photos_links[i][0], users_photos_links[i][1]])
        [this.insert(0, id_user) for this in users_photos_links]  # add user id to photo
        # TODO: save photos links

        pass
    pass


def get_links_to_photo(driver):
    photos = find_by('photos', 'public_photos', driver)
    photos_links = []
    for i in range(len(photos)):
        photos_links.append(photos[i].get_attribute('href'))
    to_exit_photos_links = []
    for number_link in range(len(photos_links)):
        driver.get(photos_links[number_link])
        s_photo = driver.find_element_by_class_name('ppp-img ')
        link_to_photo = s_photo.get_attribute('src')
        to_exit_photos_links.append([number_link, link_to_photo])
    return to_exit_photos_links


def main():
    global GRAY_USERS, COUNT_OF_BROWSER, PATH_TO_WEBDRIVER
    information('Start program.')
    user_links, users_code = load_user_links()
    GRAY_USERS = len(user_links)

    browser_pool = multiprocessing.Pool(COUNT_OF_BROWSER)
    for index_user in user_links:
        driver = webdriver.Chrome(PATH_TO_WEBDRIVER)
        browser_pool.apply_async()

    pass


if __name__ == '__main__':
    main()
