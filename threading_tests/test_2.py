from datetime import datetime
import multiprocessing

import my_csv

from selenium import webdriver


PROCESS = 3
PATH_TO_LOG = 'test.log'
PATH_TO_USERS_LINKS = 'new_users_links.csv'

PATH_TO_COUNTRY_CODE = 'all_codes_country.txt'

# LOCK = multiprocessing.Lock


def information(info):
    to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t' + info + '\n'
    print(to_write)
    with open(PATH_TO_LOG, 'a') as file:
        file.write(to_write)
    pass


def load_country_code(path=PATH_TO_COUNTRY_CODE):
    with open(path, 'r') as file:
        country_code = file.readlines()
    country_code = [this.strip() for this in country_code]
    information('Country code loaded successful.')
    return country_code


def crusher(list_to_crash, splinters):
    return [list_to_crash[i::splinters] for i in range(splinters)]


def many_sr(part_of_codes, lock):
    # global LOCK
    lock.acquire()
    try:
        driver = webdriver.Safari()
    finally:
        lock.release()
    first_page = 'http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0'

    for code in part_of_codes:
        driver.get(first_page.format(code))

        users_links_by_country = list()

        page = 1
        users_last_page = []
        while True:
            users_this_page = []
            lock.acquire()
            try:
                information(
                    'Work with {0} region, {1} page, already scrapped {2} profiles by {0}.'.format(
                        code, page, page * 15
                    )
                )
            finally:
                lock.release()
            selenium_users_on_page = driver.find_elements_by_class_name('user-link')
            for selenium_user in selenium_users_on_page:
                users_this_page.append((selenium_user.get_attribute('href'), code))

            if users_this_page == users_last_page:
                driver.close()
                set_users_links_by_country = set(users_links_by_country)
                lock.acquire()
                try:
                    my_csv.csv_data_writer(PATH_TO_USERS_LINKS, list(set_users_links_by_country))
                    information('Work with {} region finished. {} links scrapped from country'.format(
                        code, len(users_links_by_country)
                    ))
                finally:
                    lock.release()
                break
            else:
                page += 1
                # USERS_INFORMATION.extend(users_this_page)
                users_links_by_country.extend(users_this_page)
                driver.get(
                    'http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0&page={}'.format(
                        code, page
                    )
                )
                users_last_page = users_this_page.copy()
    pass


def main():
    information('Start program.')
    country_codes = load_country_code()

    spl_codes = crusher(country_codes, PROCESS)
    # lock = LOCK
    lock = multiprocessing.Lock()
    # for i in range(PROCESS):
    #     # m_process = multiprocessing.Pool.apply_async(func=many_sr, args=(spl_codes[i]))
    #     multiprocessing.Pool.apply_async(func=many_sr, args=(spl_codes[i], lock))

    # browser_list = list()
    # for i in range(PROCESS):
    #     browser_list.append(webdriver.Safari())

    for i in range(PROCESS):
        m_process = multiprocessing.Process(target=many_sr, args=(spl_codes[i], lock))
        m_process.start()
        m_process.join()


    pass


if __name__ == '__main__':
    main()
    pass