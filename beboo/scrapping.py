

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as selenium_exception


def auth(dr):
    dr.get('http://beboo.ru/auth')
    elem = dr.find_element_by_name('email')
    elem.send_keys("kozlovsky.andryu@ya.ru")
    elem1 = dr.find_element_by_name('password')
    elem1.send_keys("10bFYWH4p5")
    elem.send_keys(Keys.RETURN)
    return dr


def main():
    driver = webdriver.Safari()

    pass


if __name__ == '__main__':
    main()
