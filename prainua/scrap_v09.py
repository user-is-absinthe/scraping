# bull-it module:
from sys import exit
from re import search
from datetime import datetime


# install module:
from requests import Session
# from lxml import html
from bs4 import BeautifulSoup


def next_page(page):
    response_surname = my_sesion.post(
        url='https://pra.in.ua/uk/search/filter?page={}'.format(page),
        headers=headers,
        data={
            '_token': short_token,
            'lastname': current_surname,
            'next': '/'
        }
    )
    print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
    print('Now {} page.'.format(page))
    return response_surname


def one_sirname(sirname):
    
    global my_sesion, short_token, current_surname
    
    family_list_near = [sirname]
    
    my_sesion = Session()

    response = my_sesion.get(
        url='https://pra.in.ua/uk/login',
        headers={'User-Agent': user_agent},
    )

    regex = r"name=\"_token\" value=\"(.+)\""
    short_token = search(regex, response.text).groups()[0]

    response = my_sesion.post(
        url='https://pra.in.ua/uk/login',
        headers=headers,
        data={
            'email': 'vasyak999@yandex.ru',
            'password': '12345haha',
            '_token': short_token,
            'next': '/'
        },
    )
    print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
    print('Login successfully.' if response.status_code == 200 else 'Check login information.')
    if response.status_code != 200:
        exit(2)

    # text_file = open(path_to_exit, 'w')
    # text_file.write('Link;Surname;Father name;Year of birth;Year of death;Another year;District;Settlement\n')
    # text_file.close()

    page = 1
    for current_surname in family_list_near:

        while True:
            if page == 1:
                response_surname = my_sesion.post(
                    url='https://pra.in.ua/uk/search/filter',
                    headers=headers,
                    data={
                        '_token': short_token,
                        'lastname': current_surname,
                        'next': '/'
                    }
                )
                print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
                print('{} load successfully.'.format(
                    current_surname) if response_surname.status_code == 200 else 'Error with {}.'.format(
                    current_surname))

            else:
                response_surname = my_sesion.post(
                    url='https://pra.in.ua/uk/search/filter?page={}'.format(page),
                    headers=headers,
                    data={
                        '_token': short_token,
                        'lastname': current_surname,
                        'next': '/'
                    }
                )
            # now = datetime.now()
            print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
            print('Now {} page.'.format(page))

            content = response_surname.content
            soup = BeautifulSoup(content, "html.parser")

            table_body = soup.find('table', attrs={'class': 'table table-striped'})
            if table_body == None:
                print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
                print('{} is over. Go to next.'.format(current_surname))
                break
            rows = table_body.find_all('tr')

            for row in rows:
                columns = row.find_all('td')

                try:
                    href = columns[0].find_all('a', href=True)
                    link = href[0]['href']
                    if link != 'javascript:void(0);':
                        # print(link)
                        sirname = columns[0].find_all('b')
                        sirname = sirname[0].getText()
                        # print(sirname)
                        father_name = columns[0].find_all('small')[1]
                        father_name = str(father_name)
                        # first_in = '<small class="text-muted">Father name: ' in father_name
                        father_name = father_name[len('<small class="text-muted">Father name: '):]
                        father_name = father_name[:len(father_name) - len('</small>')]
                        # print(father_name)

                        year_of_birth = columns[1].getText()
                        year_of_birth = year_of_birth.replace('\n', '')
                        # print(year_of_birth)

                        year_of_death = columns[2].getText()
                        year_of_death = year_of_death.replace('\n', '')
                        # print(year_of_death)

                        another_year = columns[3].getText()
                        another_year = another_year.replace('\n', '')
                        # print(another_year)

                        district = columns[4].getText()
                        district = district.replace('\n\n', '\n')
                        district = district.replace('\n', ' ')
                        # print(district)

                        settlement = columns[5].getText()
                        settlement = settlement.replace('\n', '')
                        # print(settlement)

                        text_file = open(path_to_exit, 'a', encoding='utf8')
                        write_to_file = '{0};{1};{2};{3};{4};{5};{6};{7}\n'.format(
                            link,
                            sirname,
                            father_name,
                            year_of_birth,
                            year_of_death,
                            another_year,
                            district,
                            settlement
                        )
                        text_file.write(write_to_file)
                        text_file.close()
                        # print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
                        print(write_to_file)

                except IndexError:
                    pass

            page += 1

    response = my_sesion.post(
        url='https://pra.in.ua/uk/logout',
        headers=headers,
        data={
            '_token': short_token,
            'next': '/'
        },
    )

    print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
    print('Exit successfully.' if response.status_code == 200 else 'Error?')

    pass

print('Start.')
print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))

path = 'top_f.txt'
family = open(path, 'r', encoding='utf-8')
family_list = []
for i in family:
    family_list.append(i.replace('\n', ''))
print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
print('Surnames uploaded successfully.')


user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
headers = {
    'User-Agent': user_agent,
    'Referer': 'https://pra.in.ua/uk/'
    }

path_to_exit = 'exit_full.csv'

text_file = open(path_to_exit, 'w', encoding='utf8')
text_file.write('Link;Surname;Father name;Year of birth;Year of death;Another year;District;Settlement\n')
text_file.close()

for i_family in family_list:
    one_sirname(i_family)

print(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
print('End.')
