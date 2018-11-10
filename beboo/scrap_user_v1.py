import sys

from contextlib import closing
import requests
import user_agent


def load_proxies(input_file):
    with open(input_file, "r") as Fi:
        proxies = set(Fi.readlines())
    proxies = list(proxies)
    return proxies


def login(email, password, ip):
    proxy_to_login = {"http": ip}
    head_to_login = {'User-Agent': user_agent.generate_user_agent()}
    login_content = requests.session()
    answered = login_content.get(
        url='http://beboo.ru/auth',
        proxies=proxy_to_login,
        headers=head_to_login
    )
    answered_1 = login_content.post(
        url='http://beboo.ru/auth',
        proxies=proxy_to_login,
        headers=head_to_login,
        data={
            'email': 'kozlovsky.andryu@ya.ru',
            'password': '10bFYWH4p5'
        }
    )
    pass


def load_country_code(path):
    with open(path, 'r') as file:
        country_code = list(file.readline())
    return country_code


def main():
    try:
        all_country = load_country_code('all_codes_country.txt')  # list
        all_proxy = load_proxies('proxies_good.txt')  # list
    except FileNotFoundError:
        print('Proxy or region file not found.')
        sys.exit(10)

    for country in all_country:
        to_search = 'http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0&reason=0&endAge=80&startAge=18'.format(country)
        print('Now we work with {} code.'.format(country))
        counter_page = 0
        while True:
            counter_page += 1
            print('{} search page, code {}.'.format(counter_page, country))

            # page = simple_get(to_search)



        pass


if __name__ == '__main__':
    main()
