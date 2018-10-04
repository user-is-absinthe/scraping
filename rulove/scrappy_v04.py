from datetime import datetime

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.

    Попытка получить контент на `url`, выполнив HTTP-запрос GET.
    Если тип ответа контента является своего рода HTML / XML, верните
    текстовое содержимое, иначе верните «Нет».
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        # log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        log_error('Ошибка во время запроса к {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Возвращает True, если ответ похож на HTML, False в противном случае.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    Всегда полезно записывать ошибки.
    Эта функция просто печатает их.
    """
    print(e)


def parsing_acc(id_user):
    raw_html = simple_get(id_user)
    if raw_html is None:
        return id_user, 0
    html = BeautifulSoup(raw_html, 'html.parser')
    name = html.select('.anketa-name__name')
    text_name = name[0].getText()
    age = html.select('.anketa-name__age')
    text_age = age[0].getText()
    all_about = html.select('.col-xs-12 col-sm-6, .tab-anketa')
    all_about = all_about[0].select('.anketa-td')
    text_city = all_about[0].getText()
    text_gender = all_about[2].getText()
    text_body_female = all_about[3].getText()
    text_body_male = all_about[4].getText()
    text_nation = all_about[5].getText()
    want_to_search = [html.select('.search-target__gender'), html.select('.search-target__reason')]
    text_want_gender = want_to_search[0][0].getText()
    text_want_reason = want_to_search[1][0].getText()
    all_information = [id_user,
                       text_name,
                       text_age,
                       text_want_gender,
                       text_want_reason,
                       text_city,
                       text_gender,
                       text_body_female,
                       text_body_male,
                       text_nation]

    all_information_clear = []
    for m in range(len(all_information)):
        this = all_information[m]
        this1 = this.replace('\\n', '')
        # this2 = this1.replace(' ', '')
        this2 = this1.replace('                    ', '')
        this3 = this2.replace('\n', '')
        this4 = this3.replace('\t', '')
        this5 = this4.replace('                  ', '')
        this6 = this5.replace('          ', '')
        this7 = this6.replace('        ', '')
        all_information_clear.append(this7)

    print(all_information_clear)

    return all_information_clear


def to_txt(information):
    try:
        text_file = open(exit_file_name, 'a')
    except:
        text_file = open(exit_file_name, 'w')

    if tested_i == 0:
        text_file.write('Ссылка;Имя;Возраст;Ищет пол;Для;Город;Рост;Телосложение;Нация\n')

    if information[1] == 0:
        # text_file.write('{0};No data\n'.format(information[0]))
        print('No data.')
        pass
    else:
        text_file.write('{0};{1};{2};{3};{4};{5};{6};{7};{8}\n'.format(information[0], information[1], information[2], information[3], information[4], information[5], information[6], information[7], information[8]))

    text_file.close()

    pass


########################################################################################


print('Start!\nNow {}'.format(datetime.now().strftime("%B %d %Y, %H:%M:%S")))
# account = 'https://rulove.ru/anketa/40685'

# datetime.now().strftime("%B %d %Y, %H:%M:%S")

exit_file_name = 'exit_from_rulove.csv'

for tested_i in range(1000):
    # print()
    print('{}   {} user, his link is {}.'.format(datetime.now().strftime("%B %d %Y, %H:%M:%S"), tested_i, 'https://rulove.ru/anketa/' + str(tested_i)))
    info = parsing_acc('https://rulove.ru/anketa/' + str(tested_i))
    to_txt(info)


'''
проверено на первых 100 пользователях;
большая часть из них удалена.
'''