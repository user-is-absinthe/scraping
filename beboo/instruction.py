from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as selenium_exception


driver = webdriver.Chrome('C:\\Users\Worker\Pycharm\Pycharm_project\scraping\\beboo\chromedriver')  # Optional argument, if not specified will search path.

driver.get('http://beboo.ru/auth')
elem = driver.find_element_by_name('email')
elem.send_keys("kozlovsky.andryu@ya.ru")
elem1 = driver.find_element_by_name('password')
elem1.send_keys("10bFYWH4p5")
elem.send_keys(Keys.RETURN)

driver.get('http://beboo.ru/search?iaS=0&status=all&country=RU&region=all&town=all&lookFor=0')
users_on_page = driver.find_elements_by_class_name('user-link')
next_page = driver.find_element_by_link_text('Следующие >')

users_on_page[0].click()
name = driver.find_element_by_class_name('profile-nick-name').text.partition('\n')[0]
# name = name.text.partition('\n')[0]
sex = driver.find_element_by_id('val_age').text # driver.find_elements_by_tag_name('dd')[0].text
type_of_account = driver.find_elements_by_tag_name('dd')[1].text.lower()
age = driver.find_elements_by_tag_name('dd')[2].text
# country = from for
city = driver.find_elements_by_tag_name('dd')[4].text
about = driver.find_elements_by_tag_name('p')[6].text
find = driver.find_elements_by_tag_name('p')[7].text  # кого ищет

# about
family = driver.find_element_by_id('val_25').text  # семейное положение
profit = driver.find_element_by_id('val_26').text  # доход
financial_situation = driver.find_element_by_id('val_27').text  # материальное положение
accommodation = driver.find_element_by_id('val_28').text  # проживание	
auto = driver.find_element_by_id('val_29').text  # наличие автомобиля	
smoke = driver.find_element_by_id('val_30').text  # отношение к курению	
alco = driver.find_element_by_id('val_31').text  # отношение к алкоголю	
language = driver.find_element_by_id('val_32').text  # знание языков

# look
height = driver.find_element_by_id('val_height').text.replace(' см', '')  # рост, см
weight = driver.find_element_by_id('val_weight').text.replace(' кг', '')  # вес, кг
head_color = driver.find_element_by_id('val_23').text  # цвет волос
eye_color = driver.find_element_by_id('val_24').text  # цвет глаз
body = driver.find_element_by_id('val_19').text  # телосложение	
tatoo = driver.find_element_by_id('val_20').text  # татуировки	
piercing = driver.find_element_by_id('val_21').text  # пирсинг !!!
other_hair = driver.find_element_by_id('val_22').text  # волосы на лице и на теле

# sexual preferences
orientation = driver.find_element_by_id('val_33').text  # ориентация	
type_of_sex = driver.find_element_by_id('val_35').text  # тип секса	
role_of_sex = driver.find_element_by_id('val_34').text  # роль	
favorite_poses_in_sex = driver.find_element_by_id('val_36').text  # позы	
to_do = driver.find_element_by_id('val_37').text  # действия !!!
erogenous_zones = driver.find_element_by_id('val_38').text  # эрогенные зоны
fetishes = driver.find_element_by_id('val_39').text  # фетиши

# photos
photos = driver.find_elements_by_class_name('public_photos')
photos[0].click()
photo = driver.find_element_by_class_name('ppp-img ')
link_to_photo = photo.get_attribute('src')
link_to_photo = photo.get_attribute('src').replace('800x800', '1200x1200')
# TODO: open new tab & work with new tab
# open new tab to test big img
driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 





try:
    piercing = driver.find_element_by_id('val_21').text
except selenium_exception.NoSuchElementException:
    print(0)
