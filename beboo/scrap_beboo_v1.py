

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


def main():

    counter = 0
    max_user = 100
    while True:

        if counter == max_user:
            break
        counter += 1
    pass


if __name__ == '__main__':
    main()

    # TODO: адекватный обход по id сделать не получиться, НУЖНО перебирать страны, внутри стран страницы и так далее
    # страна - страница (проверка уникальности) - пользователи
