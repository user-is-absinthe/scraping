
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

########################################################################################


print('Start!')
account = 'https://rulove.ru/anketa/39918'

raw_html = simple_get(account)

html = BeautifulSoup(raw_html, 'html.parser')

name = html.select('.anketa-name__name')
text_name = name[0].getText()

age = html.select('.anketa-name__age')
text_age = age[0].getText()

# gender = html.select('.tab-anketa, .anketa-td')

# all_about = html.select('.col-xs-12 col-sm-6, .tab-anketa')
all_about = html.select('.col-xs-12 col-sm-6, .tab-anketa')
all_about = all_about[0].select('.anketa-td')
# text_about = all_about[0].getText()
text_city = all_about[0].getText()
text_gender = all_about[2].getText()
text_body_female = all_about[3].getText()
text_body_male = all_about[4].getText()
text_nation = all_about[5].getText()

# all_about_2 = html.select('.col-xs-12 col-sm-6, .tab-anketa second, .anketa-td')
# city = html.select('.anketa-name__city')

want_to_search = [html.select('.search-target__gender'), html.select('.search-target__reason')]
text_want_gender = want_to_search[0][0].getText()
text_want_reason = want_to_search[1][0].getText()
# body =

# print('name ', name[0].getText())
# print('age ', age[0].getText())
# print(want_to_search[0][0].getText(), want_to_search[1][0].getText())
# print('all_about_1 ', all_about[0].getText())
# print('all_about_2 ', all_about[1].getText())
# print('city ', city[0].getText())

# print(text_about)

all_information = [account,
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
for i in range(len(all_information)):
    this = all_information[i]
    this1 = this.replace('\\n', '')
    this2 = this1.replace(' ', '')
    this3 = this2.replace('\n', '')
    this4 = this3.replace('\t', '')
    all_information_clear.append(this4)

print(all_information_clear)

# print(html.select('.anketa-name__name'))
