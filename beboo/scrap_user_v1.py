

from contextlib import closing
from requests import get
from requests.exceptions import RequestException


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


def load_proxies(input_file):
    with open(input_file, "r") as Fi:
        proxies = set(Fi.readlines())

    proxies = list(proxies)
    for proxy in proxies:
        pass
    return proxies


def login():
    pass


def main():
    all_country = open('all_codes_country.txt', 'r')
    all_proxy = load_proxies(input_file='proxies_good.txt')

    for country in all_country:
        to_search = 'http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0&reason=0&endAge=80&startAge=18&aS%5B25%5D%5B%5D=0&aS%5B26%5D%5B%5D=0&aS%5B28%5D%5B%5D=0&aS%5B29%5D%5B%5D=0&aS%5B27%5D%5B%5D=0&aS%5B32%5D%5B%5D=0&aS%5B30%5D%5B%5D=0&aS%5B31%5D%5B%5D=0&height=0&height=0&aS%5B19%5D%5B%5D=0&aS%5B23%5D%5B%5D=0&aS%5B24%5D%5B%5D=0&aS%5B20%5D%5B%5D=0&aS%5B21%5D%5B%5D=0&aS%5B22%5D%5B%5D=0&aS%5B33%5D%5B%5D=0&aS%5B35%5D%5B%5D=0&aS%5B34%5D%5B%5D=0'.format(country)
        print('Now we work with {} code.'.format(country))
        counter_page = 0
        while True:
            counter_page += 1
            print('{} search page, code {}.'.format(counter_page, country))

            page = simple_get(to_search)



        pass


if __name__ == '__main__':
    main()
