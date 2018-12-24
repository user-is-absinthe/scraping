from datetime import datetime
import os

import my_csv

from selenium import webdriver

PATH_TO_DATA = 'data'

PATH_TO_COUNTRY_CODE = 'all_codes_country.txt'
PATH_TO_DRIVER = 'C:\\Users\Worker\Pycharm\Pycharm_project\scraping\\beboo\chromedriver'

PATH_TO_LOG = PATH_TO_DATA + '/users_links.log'
PATH_TO_USERS_LINKS = PATH_TO_DATA + '/users_links.csv'

ALL_LINKS = 0


if not os.path.exists(PATH_TO_DATA):
    os.makedirs(PATH_TO_DATA)


def load_country_code(path=PATH_TO_COUNTRY_CODE):
    with open(path, 'r') as file:
        country_code = file.readlines()
    country_code = [this.strip() for this in country_code]
    information('Country code loaded successful.')
    return country_code


def information(info):
    to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t' + info + '\n'
    print(to_write)
    with open(PATH_TO_LOG, 'a') as file:
        file.write(to_write)
    pass


def get_links(first_page, country):
    global ALL_LINKS
    driver = webdriver.Chrome(PATH_TO_DRIVER)
    driver.get(first_page)

    users_links_by_country = list()

    page = 1
    users_last_page = []
    while True:
        users_this_page = []
        information(
            'Work with {0} region, {1} page, already scrapped {2} profiles by {0}, from other regions {3}.'.format(
                country, page, page * 15, ALL_LINKS
            )
        )
        selenium_users_on_page = driver.find_elements_by_class_name('user-link')
        for selenium_user in selenium_users_on_page:
            users_this_page.append((selenium_user.get_attribute('href'), country))
        if users_this_page == users_last_page:
            driver.close()
            set_users_links_by_country = set(users_links_by_country)
            my_csv.csv_data_writer(PATH_TO_USERS_LINKS, list(set_users_links_by_country))
            information('Work with {} region finished. {} links scrapped from country'.format(
                country, len(users_links_by_country)
            ))
            ALL_LINKS += len(users_links_by_country)
            break
        else:
            page += 1
            # USERS_INFORMATION.extend(users_this_page)
            users_links_by_country.extend(users_this_page)
            driver.get(
                'http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0&page={}'.format(
                    country, page
                )
            )
            users_last_page = users_this_page.copy()

    pass


def main():
    information('Start program.')
    country_codes = load_country_code()

    # driver = webdriver.Chrome(PATH_TO_DRIVER)

    for code in country_codes:
        first_page = 'http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0'.format(code)
        get_links(first_page, code)

    # my_csv.csv_data_writer(PATH_TO_USERS_LINKS, USERS_INFORMATION)
    pass


if __name__ == '__main__':
    main()
