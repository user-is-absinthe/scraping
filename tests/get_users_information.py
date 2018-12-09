from datetime import datetime
import os

import my_csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as selenium_exception


USER_NAME = '2811'
PATH_TO_DATA = 'data'

# PATH_TO_USERS_LINKS = PATH_TO_DATA + '/users_links.csv'
PATH_TO_USERS_LINKS = 'test.csv'
PATH_TO_LOG = PATH_TO_DATA + '/' + USER_NAME + '_users.log'
PATH_TO_USERS_INFORMATION = PATH_TO_DATA + '/' + USER_NAME + '_users.csv'
PATH_TO_PHOTOS_LINKS = PATH_TO_DATA + '/photos_links_from_' + USER_NAME + '.csv'
PATH_TO_PHOTOS = PATH_TO_DATA + '/photos'
PATH_TO_TEMP_DIR = PATH_TO_DATA + '/temp'

# PATH_TO_WEBDRIVER = os.path.abspath('chromedriver.exe')
PATH_TO_WEBDRIVER = 'C:\\Users\Worker\Pycharm\Pycharm_project\scraping\\beboo\chromedriver'

if not os.path.exists(PATH_TO_DATA):
    os.makedirs(PATH_TO_DATA)
if not os.path.exists(PATH_TO_PHOTOS):
    os.makedirs(PATH_TO_PHOTOS)
if not os.path.exists(PATH_TO_TEMP_DIR):
    os.makedirs(PATH_TO_TEMP_DIR)

GRAY_USERS = 0
WHITE_USERS = 0
BLACK_USERS = 0
ALL_PROXY = list()


def information(info):
    to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t' + info + '\n'
    print(to_write)
    with open(PATH_TO_LOG, 'a') as file:
        file.write(to_write)
    pass


def write_csv_head():
    if not os.path.exists(PATH_TO_USERS_INFORMATION):
        my_csv.csv_line_writer(PATH_TO_USERS_INFORMATION,
                               [
                                   'id_user', 'link_to_user', 'имя', 'пол', 'тип аккаунта', 'возраст', 'страна',
                                   'город', 'о себе', 'кого ищет', 'семейное положение', 'доход',
                                   'материальное положение', 'проживание', 'наличие автомобиля', 'отношение к курению',
                                   'отношение к алкоголю', 'знание языков', 'рост, см', 'вес, кг', 'цвет волос',
                                   'цвет глаз', 'телосложение', 'татуировки', 'пирсинг', 'волосы на лице и на теле',
                                   'ориентация', 'тип секса', 'роль', 'позы', 'действия', 'эрогенные зоны', 'фетиши'
                               ]
                               )
        information('CSV users info head created successful.')
    if not os.path.exists(PATH_TO_PHOTOS_LINKS):
        my_csv.csv_line_writer(PATH_TO_PHOTOS_LINKS, ['id_user', 'number_of_photo', 'link_to_photo'])
        information('CSV photos links head created successful.')
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
        if param_name == 'bad_username':
            return dr.find_element_by_class_name(param_text).text
        if param_name == 'class':
            return dr.find_element_by_class_name(param_text).get_attribute('textContent')
        elif param_name == 'id':
            return dr.find_element_by_id(param_text).get_attribute('textContent')
        elif param_name == 'tag_1':
            return dr.find_elements_by_tag_name(param_text)[1].get_attribute('textContent').lower()
        elif param_name == 'tag_2':
            return dr.find_elements_by_tag_name(param_text)[2].get_attribute('textContent')
        elif param_name == 'tag_4':
            return dr.find_elements_by_tag_name(param_text)[4].get_attribute('textContent')
        elif param_name == 'tag_6':
            return dr.find_elements_by_tag_name(param_text)[6].get_attribute('textContent')
        elif param_name == 'tag_7':
            return dr.find_elements_by_tag_name(param_text)[7].get_attribute('textContent')
        elif param_name == 'photos':
            return dr.find_elements_by_class_name(param_text)
    except selenium_exception.NoSuchElementException:
        return 'nd'
    except IndexError:
        information('WARNING!\tIndex error.')
        return 'Index Error.'


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


def scr_user(dr, number_user, link_to_user, region_code):
    global GRAY_USERS, WHITE_USERS, BLACK_USERS, PATH_TO_USERS_INFORMATION, PATH_TO_TEMP_DIR
    dr.get(link_to_user)
    try:
        dr.find_element_by_class_name('info-404')
        BLACK_USERS += 1

    except selenium_exception.NoSuchElementException:
        WHITE_USERS += 1
        id_user = link_to_user.replace('http://beboo.ru/profile/', '').replace('?from=1', '')

        information(
            'User {} (user id is {}) is scrapped with photo(-s). Now {}/{} users done ({}%), {} is dead.'.format(
                        number_user + 1,
                        id_user,
                        WHITE_USERS,
                        GRAY_USERS,
                        round(((number_user + 1 + BLACK_USERS) / GRAY_USERS) * 100, 2),
                        BLACK_USERS
            )
        )

        name = find_by('bad_username', 'profile-nick-name', dr).partition('\n')[0]
        sex = find_by('id', 'val_age', dr)
        type_of_account = find_by('tag_1', 'dd', dr)
        age = find_by('tag_2', 'dd', dr)
        country = region_code
        # country = '1'  # сделать подстановку из словаря, ищем по строке
        # driver.find_element_by_class_name('look_for').text и если совпадает со страной из списка, подставляем её
        city = find_by('tag_4', 'dd', dr)
        about = find_by('tag_6', 'p', dr).replace('\n', '; ')
        find = find_by('tag_7', 'p', dr).replace('\n', '; ')

        # about
        # additionally = dr.find_element_by_name('advTab')
        # additionally.click()
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

        my_csv.csv_line_writer(PATH_TO_USERS_INFORMATION, [
            id_user, link_to_user, name, sex, type_of_account, age, country, city, about, find, family, profit,
            financial_situation, accommodation, auto, smoke, alco, language, height, weight, head_color, eye_color,
            body, tatoo, piercing, other_hair, orientation, type_of_sex, role_of_sex, favorite_poses_in_sex, to_do,
            erogenous_zones, fetishes
        ])

        users_photos_links = get_links_to_photo(dr)

        [this.insert(0, id_user) for this in users_photos_links]  # add user id to photo
        #  save photos links
        for index in range(len(users_photos_links)):
            save_photo_links(users_photos_links[index])

        my_csv.csv_data_writer(PATH_TO_TEMP_DIR + '/{}.scv'.format(id_user), users_photos_links)
        pass
    pass


def save_photo_links(photo_inform):
    global PATH_TO_PHOTOS_LINKS
    u_id = photo_inform[0]  # user id
    number = photo_inform[1]  # number photo from user
    photo_link = photo_inform[2]  # link to photo
    my_csv.csv_line_writer(PATH_TO_PHOTOS_LINKS, [u_id, number, photo_link])
    pass


def main():
    information('Start program.')
    global PATH_TO_WEBDRIVER, GRAY_USERS, ALL_PROXY
    user_links, users_code = load_user_links()
    GRAY_USERS = len(user_links)
    driver = webdriver.Chrome(PATH_TO_WEBDRIVER)
    driver = auth(driver)
    write_csv_head()

    for index in range(len(user_links)):
        scr_user(
            dr=driver,
            number_user=index,
            link_to_user=user_links[index],
            region_code=users_code[index]
        )

    information('That`s all!')
    pass


if __name__ == '__main__':
    main()
