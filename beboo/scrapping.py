import sys
# import random
import csv
# import time
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as selenium_exception
import requests


path_to_users_links = 'data/users_links.csv'
path_to_users_information = 'data/users.csv'
path_to_photos_links = 'data/photos_links.csv'
path_to_log = 'data/beboo.log'
path_to_photos = 'data/photos'

path_to_country_code = 'all_codes_country.txt'

u_id = 0
region_code = ''
users_links = []
users_alive = 0
count_of_unique_users_links = 0


def to_log(info):
    global path_to_log
    with open(path_to_log, 'a') as file:
        to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t' + info + '\n'
        file.write(to_write)
    pass


def auth(dr):
    dr.get('http://beboo.ru/auth')
    elem = dr.find_element_by_name('email')
    elem.send_keys("kozlovsky.andryu@ya.ru")
    elem1 = dr.find_element_by_name('password')
    elem1.send_keys("10bFYWH4p5")
    elem.send_keys(Keys.RETURN)
    print('Authorization successful.')
    to_log('Authorization successful.')
    return dr


def load_country_code(path):
    with open(path, 'r') as file:
        country_code = file.readlines()
    country_code = [this.strip() for this in country_code]
    to_log('Country code loaded successful.')
    return country_code


def write_csv(path, data):
    with open(path, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for line in data:
            writer.writerow(line)
    print('CSV in {} created successful!'.format(path))
    pass


def write_csv_head(path, head):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for line in head:
            writer.writerow(line)
    pass


def create_head():
    global path_to_users_links, path_to_users_information, path_to_photos_links
    write_csv_head(path_to_users_links, [['id_user', 'link_to_user']])
    write_csv_head(
        path_to_users_information,
        [[
            'id_user', 'link_to_user', 'имя', 'пол', 'тип аккаунта', 'возраст', 'страна',
            'город', 'о себе', 'кого ищет', 'семейное положение', 'доход', 'материальное положение',
            'проживание', 'наличие автомобиля', 'отношение к курению', 'отношение к алкоголю', 'знание языков',
            'рост, см', 'вес, кг', 'цвет волос', 'цвет глаз', 'телосложение', 'татуировки', 'пирсинг',
            'волосы на лице и на теле', 'ориентация', 'тип секса', 'роль', 'позы', 'действия', 'эрогенные зоны',
            'фетиши'
        ]]
    )
    write_csv_head(path_to_photos_links, [['id_user', 'link_to_photo']])
    print('CSV head created successful!')
    to_log('CSV head created successful.')
    pass


def users_on_page(dr):
    # users_links_set = set()
    page = 1
    users_last_page = []
    global region_code, users_links
    while True:
        users_this_page = []
        print('Work with {} region, {} page, already scrapped {} profiles.'.format(
            region_code, page, page * 15
        ))
        to_log('Work with {} region, {} page, already scrapped {} profiles.'.format(
            region_code, page, page * 15
        ))
        selenium_users_on_page = dr.find_elements_by_class_name('user-link')
        for selenium_user in selenium_users_on_page:
            # users_links_set.add(selenium_user.get_attribute('href'))
            # users_links.append(selenium_user.get_attribute('href'))
            users_this_page.append(selenium_user.get_attribute('href'))
        # time.sleep(random.uniform(2, 5))
        if users_this_page == users_last_page:
            break
        else:
            page += 1
            users_links.extend(users_this_page)
            dr.get('http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0&page={}'.format(
                region_code, page
            ))
            users_last_page = users_this_page.copy()
        # try:
        #     next_page = dr.find_element_by_link_text('Следующие >')
        #     # time.sleep(random.uniform(0, 3))
        #     next_page.click()
        #     page += 1
        # except selenium_exception.NoSuchElementException:
        #     break

    # users_links = list(users_links_set)
    # user_id_links = []
    # global user_id
    # for user_link in users_links:
    #     user_id_links.append([user_id, user_link])
    # write_csv(path_to_users_links, user_id_links)
    return 0


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


def load_photos(dr):
    photos = find_by('photos', 'public_photos', dr)
    photos_links = []
    for i in range(len(photos)):
        photos_links.append(photos[i].get_attribute('href'))
    for number_link in range(len(photos_links)):
        # time.sleep(random.uniform(2, 5))
        dr.get(photos_links[number_link])
        s_photo = dr.find_element_by_class_name('ppp-img ')
        link_to_photo = s_photo.get_attribute('src')
        save_photo(link_to_photo, number_link)

    pass


def save_photo(photo_link, number):
    photo_big_link = photo_link.replace('800x800', '1200x1200')
    to_save = requests.get(photo_big_link)
    if to_save.status_code == 404:
        to_save = requests.get(photo_link)
    global u_id, path_to_photos
    photo_name = path_to_photos + '/{}_{}.jpg'.format(u_id, number)  # user_id + photo number
    out = open(photo_name, "wb")
    out.write(to_save.content)
    out.close()
    write_csv(path_to_photos_links, [[number, photo_link]])
    pass


def scr_user(dr, id_user, link_to_user):
    dr.get(link_to_user)
    global path_to_users_information, region_code, count_of_unique_users_links, users_alive
    try:
        dr.find_element_by_class_name('info-404')
        # write_csv(path_to_users_information, [[id_user, 'User']])
    except selenium_exception.NoSuchElementException:
        users_alive += 1
        name = find_by('class', 'profile-nick-name', dr).partition('\n')[0]
        sex = find_by('id', 'val_age', dr)
        type_of_account = find_by('tag_1', 'dd', dr)
        age = find_by('tag_2', 'dd', dr)
        # country = region_code
        country = '1'  # сделать подстановку из словаря, ищем по строке
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

        global path_to_users_information
        write_csv(path_to_users_information, [[
            id_user, link_to_user, name, sex, type_of_account, age, country, city, about, find, family, profit,
            financial_situation, accommodation, auto, smoke, alco, language, height, weight, head_color, eye_color,
            body, tatoo, piercing, other_hair, orientation, type_of_sex, role_of_sex, favorite_poses_in_sex, to_do,
            erogenous_zones, fetishes
        ]])

        load_photos(dr)
        print('User {}/{} owned. Progress {}%.'.format(
            id_user, count_of_unique_users_links, (id_user + 1) / count_of_unique_users_links)
        )
        to_log('User {}/{} owned. Progress {}%.'.format(
            id_user, count_of_unique_users_links, (id_user + 1) / count_of_unique_users_links)
        )
        pass
    pass


def create_log():
    global path_to_log
    with open(path_to_log, 'w') as file:
        to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t' + 'Create log-file.' + '\n'
        file.write(to_write)
    pass


def main():
    to_log('Start program.')
    # user_id = 0
    # global user_id

    create_head()

    driver = webdriver.Chrome(
        'C:\\Users\Worker\Pycharm\Pycharm_project\scraping\\beboo\chromedriver'
    )  # Optional argument, if not specified will search path.
    # driver = auth(driver)

    global path_to_country_code
    try:
        all_country = load_country_code(path_to_country_code)  # list
        # all_proxy = load_proxies('proxies_good.txt')  # list
    except FileNotFoundError:
        print('Region file not found.')
        to_log('Region file not found.')
        sys.exit(10)

    global region_code
    for country in all_country:
        region_code = country
        print('Start work with {} region.'.format(region_code))
        to_log('Start work with {} region.'.format(region_code))
        driver.get('http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0'.format(country))
        users_on_page(driver)

    global users_links
    count_of_users = len(users_links)
    users_links = list(set(users_links))
    global count_of_unique_users_links
    count_of_unique_users_links = len(users_links)
    user_id_links = []
    for user_id in range(len(users_links)):
        user_id_links.append([user_id, users_links[user_id]])
    write_csv(path_to_users_links, user_id_links)
    print('Scrap all region successful. {} user links, {} unique user links.'.format(
        count_of_users, count_of_unique_users_links
    ))
    to_log('Scrap all region successful. {} user links, {} unique user links.'.format(
        count_of_users, count_of_unique_users_links
    ))

    print('Start scrapping user profiles.')
    to_log('Start scrapping user profiles.')
    driver = auth(driver)
    global u_id
    for user_id in range(len(users_links)):
        u_id = user_id
        scr_user(dr=driver, id_user=user_id, link_to_user=users_links[user_id])

    global users_alive
    print('End. {} user alive of {} all user in {} all links.'.format(
        users_alive, count_of_unique_users_links, count_of_users
    ))
    to_log('End. {} user alive of {} all user in {} all links.'.format(
        users_alive, count_of_unique_users_links, count_of_users
    ))
    driver.close()


if __name__ == '__main__':
    create_log()
    main()
    # try:
    #     main()
    # except Exception as error:
    #     print(str(error))
    #     to_log(str(error))
    #     # sys.exit(1)
