# bull-it module:
from sys import exit


# install module:
from requests import get, post


path = 'top_f.txt'
family = open(path, 'r')
family_list = []
for i in family:
    family_list.append(i.replace('\n', ''))
print('Surnames uploaded successfully.')


user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
# request = requests.get(url, headers={'User-Agent':user_agent})


response = get(
    url='https://pra.in.ua/en/',
    headers={'User-Agent':user_agent},
)
# client.get(URL)  # sets cookie
# print(response.cookies)
# if 'csrftoken' in response.cookies:
#     csrf_token = response.cookies['csrftoken']
# elif 'Cookie XSRF-TOKEN' in response.cookies['_cookies']['pra.in.ua']['/']['XSRF-TOKEN']:
#     csrf_token = response.cookies['XSRF-TOKEN']
# elif 'XSRF-TOKEN' in response.cookies:
#     csrf_token = response.cookies['XSRF-TOKEN']
# else:
#     csrf_token = response.cookies['csrf']

# csrf_token = response.cookies['_cookies']['pra.in.ua']['/']['XSRF-TOKEN']
csrf_token = response.cookies['XSRF-TOKEN']
# print(csrf_token)


response = post(
    url='https://pra.in.ua/en/login',
    # auth=('vasyak999@yandex.ru', '12345haha'),
    headers={'User-Agent':user_agent},
    data={'email': 'vasyak999@yandex.ru',
          'password': '12345haha',
          'XSRF-TOKEN': csrf_token},
    # data={'csrfmiddlewaretoken': csrf_token}
)

print(response.text)

print('Login successfully.' if response.status_code == 200 else 'Check login.')
if response.status_code != 200:
    exit(2)


# for current_surname in family_list:
#     response_surname = get('https://pra.in.ua/en/search/filter', lastname=current_surname)
#
#     pass

# data = {
#     'lastname': 'Бондаренко',
#     'csrfmiddlewaretoken': csrf_token
# }
# response_surname = post(
#     url='https://pra.in.ua/en/search/filter',
#     data=data,
#     headers={'User-Agent':user_agent}
# )
# print(response_surname.text)


response = post(
    url='https://pra.in.ua/uk/logout',
    headers={'User-Agent':user_agent},
    # data={'csrfmiddlewaretoken': csrf_token}
)
# print(response.status_code)
print(response.text)
# print('Logout successfully.' if response.status_code == 200 else 'Something went wrong.')
