from requests import Session
from bs4 import BeautifulSoup

URL = 'https://pra.in.ua/en/login'

client = Session()

html_doc = client.get(URL)

soup = BeautifulSoup(html_doc.text)
token = soup.find_all('_token')


# csrftoken = client.cookies['XSRF-TOKEN']
csrftoken = client.cookies['_token']


login_data = dict(
    username='vasyak999@yandex.ru',
    password='12345haha',
    csrfmiddlewaretoken=csrftoken,
    next='/'
)
# r = client.post(URL, data=login_data, headers=dict(Referer=URL))


r = client.post(
    url=URL,
    # auth=('vasyak999@yandex.ru', '12345haha'),
    data=dict(
        username='vasyak999@yandex.ru',
        password='12345haha',
        # csrfmiddlewaretoken=csrftoken,
        _token=csrftoken,
        next='/'
    ),
    headers=dict(
        Referer=URL,
    )
)


print(r.status_code)