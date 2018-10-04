# bull-it module:
from sys import exit
from re import search


# install module:
from requests import Session
# from lxml import html
from bs4 import BeautifulSoup


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
# print(response.status_code)
print('Login successfully.' if response.status_code == 200 else 'Check login information.')
if response.status_code != 200:
    exit(2)


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
    print('{} load successfully.'.format(current_surname) if response_surname.status_code == 200 else 'Error with {}.'.format(current_surname))
    if response.status_code != 200:
        exit(2)
    # print(response_surname.text)
    content = response_surname.content
    soup = BeautifulSoup(content, "html.parser")

    # element = soup.find('table' == 'table table-striped')
    # print(element.text)

    '''
    table = soup.find("table", {"class": "table table-striped"})
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        try:
            sirname = cells.select('target').getText()
            print(sirname)
            exit(98)
        except IndexError:
            sirname = []
            pass
        # link = cells.findAll('href')
    '''
    '''
    sirname = soup.select('a href')
    print(sirname)
    exit(98)
    '''

    data = []
    table_body = soup.find('table', attrs={'class': 'table table-striped'})
    # table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    # for row in rows:
    #     cols = row.find_all('td')
    #     cols = [ele.text.strip() for ele in cols]
    #     to_data = [ele for ele in cols if ele]
    #     # href = cols.find_all('href')
    #     # data.append(href)

    for row in rows:
        columns = row.find_all('td')
        # for column in columns:
        #     try:
        #         href = column.find_all('a', href=True)
        #         link = href[0]['href']
        #         if link != 'javascript:void(0);':
        #             print(link)
        #             # sirname = href_sirname[0]
        #             sirname = column.find_all('b')
        #             sirname = sirname[0].getText()
        #             print(sirname)
        #
        #         year_of_birth =
        #     except IndexError:
        #         pass

        try:
            href = columns[0].find_all('a', href=True)
            link = href[0]['href']
            if link != 'javascript:void(0);':
                print(link)
                # sirname = href_sirname[0]
                sirname = columns[0].find_all('b')
                sirname = sirname[0].getText()
                print(sirname)

            year_of_birth = columns[1].getText()
            year_of_birth = year_of_birth.replace('\n', '')
            print(year_of_birth)

            year_of_death = columns[2].getText()
            year_of_death = year_of_death.replace('\n', '')
            print(year_of_death)

            another_year = columns[3].getText()
            another_year = another_year.replace('\n', '')
            print(another_year)

            district = columns[4].getText()
            district = district.replace('\n\n', '\n')
            district = district.replace('\n', ' ')
            print(district)

            settlement = columns[5].getText()
            settlement = settlement.replace('\n', '')
            print(settlement)
        except IndexError:
            pass

            # exit(98)
        # print(columns)

    # print(data)
    # exit(98)


    while True:
        print('While.')
        break


    if current_surname == 'Кравец':
        print('End.')
        exit(10)

