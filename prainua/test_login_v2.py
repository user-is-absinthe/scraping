from requests import Session
import re

URL = 'https://pra.in.ua/en/login'
client = Session()
response = client.get(URL)

regex = r"name=\"_token\" value=\"(.+)\""
short_token = re.search(regex, response.text).groups()[0]

csrftoken = client.cookies['XSRF-TOKEN']
login_data = dict(username='vasyak999@yandex.ru', password='12345haha', _token=short_token, next='/')
headers = {
    'Referer': URL,
}
r = client.post(URL, data=login_data, headers=headers)
print(r.status_code)