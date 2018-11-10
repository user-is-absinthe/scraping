import sys

import requests
import user_agent


def load_proxies(input_file):
    with open(input_file, "r") as Fi:
        proxies = set(Fi.readlines())
    proxies = list(proxies)
    proxies = [this.strip() for this in proxies]
    return proxies


def load_country_code(path):
    with open(path, 'r') as file:
        country_code = list(file.readline())
    return country_code


def find_by_region(url, ip):
    proxy_now = {"http": ip}
    head_now = {'User-Agent': user_agent.generate_user_agent()}
    page_content = requests.session()
    answered = page_content.get(
        url=url,
        proxies=proxy_now,
        headers=head_now
    )
    pass


def main():
    try:
        all_country = load_country_code('all_codes_country.txt')  # list
        all_proxy = load_proxies('proxies_good.txt')  # list
    except FileNotFoundError:
        print('Proxy or region file not found.')
        sys.exit(10)

    for country in all_country:
        to_search = 'http://beboo.ru/search?iaS=0&status=all&country={}&region=all&town=all&lookFor=0'.format(country)
        print('Now we work with {} code.'.format(country))
        counter_page = 0
        while True:
            counter_page += 1
            print('{} search page, code {}.'.format(counter_page, country))

            # page = simple_get(to_search)



        pass


if __name__ == '__main__':
    main()
