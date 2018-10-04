# bull-it module:
from sys import exit
from re import search


# install module:
from requests import Session
# from lxml import html
from bs4 import BeautifulSoup


def next_page(page):
    response_surname = my_sesion.post(
        url='https://pra.in.ua/en/search/filter?page={}'.format(page),
        headers=headers,
        data={
            '_token': short_token,
            'lastname': current_surname,
            'next': '/'
        }
    )
    return response_surname


path = 'top_f.txt'
family = open(path, 'r')
family_list = []
for i in family:
    family_list.append(i.replace('\n', ''))
print('Surnames uploaded successfully.')


user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
headers={
    'User-Agent':user_agent,
    'Referer': 'https://pra.in.ua/en/'
    }

my_sesion = Session()

response = my_sesion.get(
    url='https://pra.in.ua/en/login',
    headers={'User-Agent':user_agent},
)

regex = r"name=\"_token\" value=\"(.+)\""
short_token = search(regex, response.text).groups()[0]


response = my_sesion.post(
    url='https://pra.in.ua/en/login',
    headers=headers,
    data={
        'email': 'vasyak999@yandex.ru',
        'password': '12345haha',
        '_token': short_token,
        'next': '/'
    },
)
print('Login successfully.' if response.status_code == 200 else 'Check login information.')
if response.status_code != 200:
    exit(2)


text_file = open('exit.csv', 'w')
text_file.write('Link;Surname;Father name;Year of birth;Year of death;Another year;District;Settlement\n')
text_file.close()

page = 1
for current_surname in family_list:
    response_surname = my_sesion.post(
        url='https://pra.in.ua/en/search/filter',
        headers=headers,
        data={
            '_token': short_token,
            'lastname': current_surname,
            'next': '/'
        }
    )

    while True:

        if 0 == 0:
            pass

        print('{} load successfully.'.format(current_surname) if response_surname.status_code == 200 else 'Error with {}.'.format(current_surname))
        if response.status_code != 200:
            exit(2)
        content = response_surname.content
        soup = BeautifulSoup(content, "html.parser")

        data = []
        table_body = soup.find('table', attrs={'class': 'table table-striped'})
        rows = table_body.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            print(columns)

            page += 1
            next_page(page)

            # exit(98)
        # print(columns)

    # print(data)
    # exit(98)


    if current_surname == 'Кравец':
        print('End.')
        exit(10)

