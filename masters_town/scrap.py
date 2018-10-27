import random
import sys
from user_agent import generate_user_agent
import requests
from bs4 import BeautifulSoup

#https://www.livemaster.ru/catalogue/suveniry-i-podarki
#40 elements on pages
#https://www.livemaster.ru/catalogue/suveniry-i-podarki?from=40000

#global var
mainpage = 'https://www.livemaster.ru/'
id_item = 0
id_comment = 0
id_author = 0
proxy = []
denial_of_service = 0
max_denial_of_service = 15


def load_proxies(input_file):
    with open(input_file, "r") as Fi:
        proxies = list(Fi.readlines())
    print('{} proxy load.'.format(len(proxies)))
    return proxies


def get_html(url):
    global proxy, denial_of_service, max_denial_of_service
    now_proxy = proxy[random.randint(0, len(proxy) - 1)].replace('\n', '')
    print('Now use {} proxy.'.format(now_proxy))
    in_proxy = {"http": now_proxy}
    head = {'User-Agent': generate_user_agent()}
    print('I am human: ', head['User-Agent'])
    try:
        r = requests.get(url, proxies=in_proxy, headers=head)
        denial_of_service = 0
    except:
        denial_of_service += 1
        if denial_of_service == max_denial_of_service:
            print('Too more exceptions.')
            sys.exit(20)
        else:
            print('\n\t\t\tEXCEPT n{}!!!\n'.format(denial_of_service))
            get_html(url=url)
    return r


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find_all('a', class_='pagebar__page')[-1].get('href')  #last page
    total_pages=pages.split('=')[3]
    return int(total_pages)


def img_donwload(url, index):
    name_img = './images/' + str(id_item) + '_' + str(index) + '.jpg'
    f = open(name_img, 'wb')
    f.write(get_html(url).content)
    f.close()


def write_comment(data):
    global id_comment
    file_name='./data/comments'
    try:
        file_to_csv = open(file_name + '.csv', 'a', encoding='UTF-16')
    except FileNotFoundError:
        file_to_csv = open(file_name + '.csv', 'w', encoding='UTF-16')
    if id_comment == 0:
        file_to_csv.write(
            'id_comment' + ';' + 'id_item' + ';' 'title' + ';' + 'name' + ';' + 'comment' + '\n'
        )
    id_comment = id_comment + 1
    id_comment_str = str(id_comment)
    file_to_csv.write(
        id_comment_str + ';' + data['id'] + ';' + data['title'] + ';' + data['name'] + ';' + data['comment'] + '\n'
    )
    print('comment csv success! id ' + id_comment_str)
    file_to_csv.close()


def write_csv(data):
    file_name = './data/items_list'
    try:
        file_to_csv = open(file_name + '.csv', 'a', encoding='UTF-16')
    except FileNotFoundError:
        file_to_csv = open(file_name + '.csv', 'w', encoding='UTF-16')
    if data['id_item']=='1':
        file_to_csv.write(
            'id_item' + ';' + 'path' + ';' 'title' + ';' + 'price' + ';' + 'info' + ';' + 'description' + ';'
            + 'author' + ';' + 'author_url' + ';' + 'recomend' + ';' + 'delivery' + ';' + 'return' + ';' + 'keywords'
            + ';' + 'item_url' + '\n'
        )

    file_to_csv.write(
        data['id_item'] + ';' + data['path'] + ';' + data['title'] + ';' + data['price'] + ';' + data['info'] + ';' +
        data['description'] + ';' + data['author'] + ';' + data['author_url'] + ';' + data['recomend'] + ';' +
        data['delivery'] + ';' + data['return_'] + ';' + data['key'] + ';' + data['url']+'\n'
    )
    print('\nTo csv success! New item №' + data['id_item'])
    file_to_csv.close()

def write_author(data):
    file_name = './data/author_list'
    try:
        file_to_csv = open(file_name + '.csv', 'a', encoding='UTF-16')
    except FileNotFoundError:
        file_to_csv = open(file_name + '.csv', 'w', encoding='UTF-16')
    if data['id']=='1':
        file_to_csv.write(
            'id' + ';' + 'name' + ';' + 'info' + ';' + 'description' + ';' + 'work' + 'url' +'\n'
        )

    file_to_csv.write(
        data['id'] + ';' + data['name']  + data['info'] + ';' + data['description'] + ';'+ data['work'] + ';' + data['url']+'\n'
    )
    print('\nauthor csv success!  №' + data['id'])
    file_to_csv.close()

def get_author_data(url):
    global id_author
    soup = BeautifulSoup(get_html(url).text, 'lxml')
    id_author = id_author+1
    try:
        photo = soup.find('div', class_='profile-avatar-viewer').find('img')
    except:
        photo = 'Null'
    if photo != 'Null':
        ph_url = photo.get('src')
        index = 'A' + str(id_author)
        img_donwload(ph_url, index)
    name = soup.find('section', class_='profile-user-info').find('h1').text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','')
    try:
        info =soup.find('ul', class_ ='profile-user-list').text.replace('\n',' ').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
    except:
        info = 'Null'
    try:
        work = soup.find('span', class_='work-types--title').text.replace('\n',' ').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
    except:
        work = 'Null'
    try:
        description = soup.find('div', class_ = 'profile-user-description profile-user-work-types js-text-toggle-l2 text-toggle-l2 text-toggle-12').text.split(':')
        description = description[0].replace('\n',' ').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
    except:
        description = 'Null'
    id_author_str = str(id_author)
    data_author = {'id' : id_author_str,
                   'name' : name,
                   'info' : info,
                   'description' : description,
                   'work' : work,
                   'url' : url}
    write_author(data_author)

def get_item_data(url):
    html = get_html(url).text
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('a', class_='item-block__name')
    #id_item = 0
    for item in items:
        global mainpage
        item_url = mainpage + item.get('href')
        print(item_url)
        item_soup = BeautifulSoup(get_html(item_url).text, 'lxml')
        global id_item
        id_item = id_item + 1
        try:
            photos = item_soup.find_all('a', class_ = 'photo-switcher__largephoto')
        except:
            photos = 'Null'
        if photos != 'Null':
            index = 0
            for photo in photos:
                ph_url = photo.get('href')
                index = index + 1
                img_donwload(ph_url, index)
        title = str(item_soup.find('h1', class_='item-header js-translate-item-name').text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        try:
            price = str(item_soup.find('span', class_='price').text.split('&')[0].replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','')) #+  item_soup.find('span', class_='cr js-stat-main-items-money').text
        except:
            price ='Null'
        try:
            description = str(item_soup.find('span', class_='js-translate-item-description').text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            description='Null'
        try:
            recomend = str(item_soup.find('div', class_='block__content js-translate-item-itemcare').text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            recomend = 'Null'
        try:
            return_ = str(item_soup.find('div', class_='block__content js-block-return-and-exchange').text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            return_ = str('Null')
        try:
            author = str(item_soup.find('a',class_='master__name').text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            author = 'Null'
        try:
            author_url = mainpage + item_soup.find('a',class_='master__name').get('href') + '/profile'
        except:
            author_url = 'Null'
        if author_url != 'Null':
            get_author_data(author_url)
        try:
            infos = item_soup.find_all('li', class_='item-info__item')
        except:
            infos = 'Null'
        if infos != 'Null':
            info = ''
            for inf in infos:
                info = info + inf.text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','')
        else:
            info = 'Null'
        try:
            delivery = item_soup.find('div', class_='item-page-desc-block-text-delivery').text.replace('\n',' ').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
        except:
            delivery = 'Null'
        try:
            pay = item_soup.find('div', class_ ='payment-main-box').text.replace('\n',' ').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
        except:
            pay = 'Null'
        try:
            keywords = item_soup.find('ul', class_='tag-list').text.replace('\n',' ').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
        except:
            keywords = 'Null'
        id_item_str = str(id_item)
        try:
            comments = item_soup.find_all('div', class_='master-reviews__feedback')
            names = item_soup.find_all('span',itemprop='name') # names[3] = name first user
        except:
            comments = 'Null'
            names ='Null'
        if comments != 'Null' and names !='Null':
            j=3
            for comment in comments:
                comment= comment.text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','')
                try:
                    name = names[j].text.replace('\n', '').replace(',', '').replace('\t', '').replace('\r', '').replace('"', '').replace('\\U', '').replace(';', '')
                except IndexError:
                    name = 'Null'
                j = j + 1
                data_coment = {'id' : id_item_str,
                               'title': title,
                               'name' : name,
                               'comment' : comment}
                write_comment(data_coment)
        try:
            path = item_soup.find('a', class_='breadcrumbs__link').text
        except:
            path = 'Null'
        path = path + '>' + names[0].text + '>' + names[1].text + '>' + names[2].text
        id_item_str = str(id_item)
        item_url_str = str(item_url)
        data = {'id_item': id_item_str,
                'path': path,
                'title': title,
                'price': price,
                'info': info,
                'description': description,
                'author' : author,
                'author_url' : author_url,
                'recomend': recomend,
                'delivery' : delivery,
                'pay' : pay,
                'return_': return_,
                'key' : keywords,
                'url': item_url_str}

        print(data)
        write_csv(data)


def main():
    base_url = 'https://www.livemaster.ru/catalogue/suveniry-i-podarki?from='
    global proxy
    proxy = load_proxies('proxies_good.txt')
    total_pages = get_total_pages(get_html(base_url).text)

    for i in range (0, total_pages + 40, 40): #to all pages
    #for i in range(0, 40, 40): #for test
        url_gen = base_url + str(i)
        # get_html(url_gen)
        get_item_data(url_gen)


if __name__ == '__main__':
    main()