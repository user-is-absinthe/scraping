# bull-it module:
# from sys import exit


# install module:
from requests import Session


# path = 'top_f.txt'
# family = open(path, 'r')
# family_list = []
# for i in family:
#     family_list.append(i.replace('\n', ''))
# print('Surnames uploaded successfully.')


user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')

my_sesion = Session()

my_sesion.get(
    url='https://pra.in.ua/en/login',
    headers={'User-Agent':user_agent},
)

csrf_token = my_sesion.cookies['XSRF-TOKEN']

response = my_sesion.post(
    url='https://pra.in.ua/en/login',
    headers={
        'User-Agent':user_agent,
        'Referer': 'https://pra.in.ua/en/'
    },
    data={'email': 'vasyak999@yandex.ru',
          'password': '12345haha',
          'XSRF-TOKEN': csrf_token},
)

print(response.text)

# print('Login successfully.' if response.status_code == 200 else 'Check login information.')
# if response.status_code != 200:
#     exit(2)


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

#
# response.post(
#     url='https://pra.in.ua/uk/logout',
#     headers={'User-Agent':user_agent},
#     # data={'csrfmiddlewaretoken': csrf_token}
# )
# # print(response.status_code)
# print(response.text)
# print('Logout successfully.' if response.status_code == 200 else 'Something went wrong.')
