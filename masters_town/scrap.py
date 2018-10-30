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
max_denial_of_service = 5
max_missed_together = 5

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
    print('I am human: ', head)
    try:
        r=requests.get(url, proxies=in_proxy, headers = head)
        denial_of_service = 0
    except Exception as er:
        print(er)
        denial_of_service += 1
        if denial_of_service == max_denial_of_service:
            print('Too more exceptions.')
            #sys.exit(20)
            return False
        else:
            print('\t\t\tEXCEPT n{}!!!'.format(denial_of_service))
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
            'id_comment' + ';' + 'id_item' + ';' 'title' + ';' + 'name' + ';' + 'date' + ';'+ 'comment' + '\n'
        )
    id_comment = id_comment + 1
    id_comment_str = str(id_comment)
    file_to_csv.write(
        id_comment_str + ';' + data['id'] + ';' + data['title'] + ';' + data['name'] + ';' + data['date'] + ';'+ data['comment'] + '\n'
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
            'id_item' + ';' + 'path' + ';' 'title' + ';' + 'price' + ';' + 'inf_form' + ';' + 'inf_time' + ';'
            + 'inf_mat' + ';' + 'inf_size' + ';' + 'description' + ';' + 'author' + ';' + 'author_url' +';' + 'recomend'
            + ';' + 'delivery' + ';' + 'pay' + ';' + 'return' + ';' + 'keywords' + ';' + 'item_url' + '\n'
        )

    file_to_csv.write(
        data['id_item'] + ';' + data['path'] + ';' + data['title'] + ';' + data['price'] + ';' + data['inf_form'] + ';'
        + data['inf_time'] + ';' + data['inf_mat'] + ';' + data['inf_size'] + ';' +  data['description'] + ';'+ data['author']
        + ';' + data['author_url'] + ';' + data['recomend'] + ';' + data['delivery'] + ';' + data ['pay'] + ';'
        + data['return_'] + ';' + data['key'] + ';' + data['url']+'\n'
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
            'id' + ';' + 'name' + ';' + 'inf_loc' + ';' + 'inf_time' + ';' + 'inf_shop' + ';' + 'inf_works' + ';'
            + 'description' + ';' + 'work' + ';' + 'url' +'\n'
        )

    file_to_csv.write(
        data['id'] + ';' + data['name']+ ';' + data['inf_loc'] + ';' + data['inf_time'] + ';' + data['inf_shop'] + ';'
        + data['inf_works'] + ';'+ data['description'] + ';'+ data['work'] + ';' + data['url']+'\n'
    )
    print('\nauthor csv success!  №' + data['id'])
    file_to_csv.close()

def get_author_data(url):
    global id_author
    try:
        html_a = get_html(url).text
    except:
        print('Authors problem ',url)
        return False
    soup = BeautifulSoup(html_a, 'lxml')
    id_author = id_author+1
    try:
        photo = soup.find('div', class_='profile-avatar-viewer').find('img')
    except:
        photo = ''
    if photo != '':
        ph_url = photo.get('src')
        index = 'A' + str(id_author)
        try:
            img_donwload(ph_url, index)
        except Exception as er:
            print(er)
            ph_url = mainpage + ph_url #https://www.livemaster.ru/image/empty/avatars/unknown_userX245.png?03102016
            img_donwload(ph_url, index)
    name = soup.find('section', class_='profile-user-info').find('h1').text.replace('\n','').replace(',','').replace(
        '\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','')
    try:#inf_loc inf_time inf_shop inf_works
        info = soup.find('ul', class_='profile-user-list').find_all('li')
        print(info)
        for j in range(len(info)):
            info[j] = info[j].text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace(
                '"','').replace('\\U','').replace(';','')
        inf_loc = info[0]
        inf_time = info[1]
        inf_shop = info[2]
        inf_works = info[3]
    except:
        inf_loc = ''
        inf_time = ''
        inf_shop = ''
        inf_works = ''
    # try:
    #     work = soup.find('span', class_='work-types--title').text.replace('\n',' ').replace(',','').replace(
    #         '\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
    # except:
    #     work = ''
    try:
        description = soup.find('div', class_ = 'profile-user-description profile-user-work-types js-text-toggle-l2 text-toggle-l2 text-toggle-12')#.text.split(':')
        description = str(description)
        description_list = description.split('<span')
        print(description_list)
        for j in range(len(description_list)):
            description_list[j] = BeautifulSoup(description_list[j], 'lxml').text.replace('\n', ' ').replace('\\U', '').replace(
                ';', '').replace('"', '').replace(',', '').replace('\t', '').replace('  ', ' ')
        des = description_list[1].split('>')
        work = des[1].replace('\n','').replace('\r','')
        description = description_list[0].replace('\n','').replace('\r','')
    except:
        description = ''
        work = ''
    id_author_str = str(id_author)
    data_author = {'id' : id_author_str,
                   'name' : name,
                   'inf_loc' : inf_loc,
                   'inf_time': inf_time,
                   'inf_shop': inf_shop,
                   'inf_works': inf_works,
                   'description' : description,
                   'work' : work,
                   'url' : url}
    write_author(data_author)

def get_item_data(html):
    #html = get_html(url).text
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('a', class_='item-block__name')
    #id_item = 0
    for item in items:
        global mainpage, max_missed_together
        item_url = mainpage + item.get('href')
        print(item_url)
        try:
            item_html = get_html(item_url).text
            tries = 0
        except Exception as er:
            print(er)
            tries = tries + 1
            if tries < max_missed_together:
                continue
            else:
                print('Max_missed_together_item')
                sys.exit(21)
        item_soup = BeautifulSoup(item_html, 'lxml')
        global id_item
        id_item = id_item + 1
        try:
            photos = item_soup.find_all('a', class_ = 'photo-switcher__largephoto')
        except:
            photos = ''
        if photos != '':
            index = 0
            for photo in photos:
                ph_url = photo.get('href')
                index = index + 1
                try:
                    img_donwload(ph_url, index)
                except Exception as er:
                    print(er)
                    continue
        title = str(item_soup.find('h1', class_='item-header js-translate-item-name').text.replace('\n','').replace(
            ',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        try:
            price = str(item_soup.find('span', class_='price').text.split('&')[0].replace('\n','').replace(
                ',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            price =''
        try:
            description = str(item_soup.find('span', class_='js-translate-item-description').text.replace(
                '\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            description=''
        try:
            recomend = str(item_soup.find('div', class_='block__content js-translate-item-itemcare').text.replace(
                '\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            recomend = ''
        try:
            return_ = str(item_soup.find('div', class_='block__content js-block-return-and-exchange').text.replace(
                '\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            return_ = str('')
        try:
            author = str(item_soup.find('a',class_='master__name').text.replace('\n','').replace(',','').replace(
                '\t','').replace('\r','').replace('"','').replace('\\U','').replace(';',''))
        except:
            author = ''
        try:
            author_url = mainpage + item_soup.find('a',class_='master__name').get('href') + '/profile'
        except:
            author_url = ''
        if author_url != '':
            get_author_data(author_url)
        try:
            infos = item_soup.find_all('li', class_='item-info__item')
        except:
            infos = ''# info: form [time] materials size
        if infos != '':
            info = []
            j = 0
            for inf in infos:
                info.append(inf.text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace(
                    '"','').replace('\\U','').replace(';',''))
                j = j+1
            inf_form = info[0]
            if j == 4:
                inf_time = info[1]
                inf_mat=info[2]
                inf_size=info[3]
            elif j==3:
                inf_time = ''
                inf_mat = info[1]
                inf_size = info[2]
            elif j == 2:
                inf_time = ''
                inf_mat = info[1]
                inf_size = ''
        else:
            inf_form = ''
            inf_time = ''
            inf_mat = ''
            inf_size = ''
        try:
            delivery = item_soup.find('div', class_='item-page-desc-block-text-delivery')
            #print(type(delivery))
            delivery = str(delivery)
            #print(type(delivery))
            delivery_list = delivery.split('<strong>')
            delivery = ''
            for j in range(len(delivery_list)):
                delivery_list[j] = BeautifulSoup(delivery_list[j], 'lxml').text.replace('\n',' ').replace(
                    '\\U','').replace(';','').replace('"','').replace(',','').replace('\t','').replace('  ',' ')
                #print(delivery_list[j])
                delivery = delivery + '\t' + delivery_list[j]
            delivery = delivery.replace('\t\t', ' ').replace('\n','').replace('\r','')
            #print(delivery)
        except Exception as er:
            #print(er)
            delivery = ''
        try:
            pay = item_soup.find('div', class_ ='payment-main-box').text.replace(',','').replace('\r','').replace(
                '\n','\t').replace('"','').replace('\\U','').replace(';','').replace('\t\t',' ').replace('\n','')
            #print(pay)
        except:
            pay = ''
        try:
            keywords = item_soup.find('ul', class_='tag-list').text.replace('\n',' ').replace(',','').replace(
                '\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','').replace('  ',' ')
        except:
            keywords = ''
        id_item_str = str(id_item)
        try:
            comments = item_soup.find_all('div', class_='master-reviews__feedback')
            names = item_soup.find_all('span',itemprop='name') # names[3] = name first user
            dates = item_soup.find_all('span', class_='master-reviews__date')
        except:
            comments = ''
            names =''
            dates = ''
        if comments != '' and names !='' and dates != '':
            j=3
            for comment in comments:
                try:
                    comment= comment.text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace(
                        '"','').replace('\\U','').replace(';','')
                except:
                    comment = ''
                try:
                    name = names[j].text.replace('\n', '').replace(',', '').replace('\t', '').replace('\r', '').replace(
                        '"', '').replace('\\U', '').replace(';', '')
                except IndexError:
                    name = ''
                try:
                    date = dates[j-3].text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace(
                        '"','').replace('\\U','').replace(';','')
                except:
                    date = ''
                j = j + 1
                data_coment = {'id' : id_item_str,
                               'title': title,
                               'name' : name,
                               'date' : date,
                               'comment' : comment}
                write_comment(data_coment)
        try:
            path = item_soup.find('a', class_='breadcrumbs__link').text
        except:
            path = ''
        path = path + '>' + names[0].text + '>' + names[1].text + '>' + names[2].text
        id_item_str = str(id_item)
        item_url_str = str(item_url)
        data = {'id_item': id_item_str,
                'path': path,
                'title': title,
                'price': price,
                'inf_form': inf_form,
                'inf_time': inf_time,
                'inf_mat': inf_mat,
                'inf_size': inf_size,
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
    global proxy, max_missed_together
    proxy = load_proxies('proxies_good.txt')
    total_pages = get_total_pages(get_html(base_url).text)

    for i in range (0, total_pages + 40, 40): #to all pages
    # for i in range(0, 40, 40): #for test
        url_gen = base_url + str(i)
        try:
            html = get_html(url_gen).text
            tries = 0
        except Exception as er:
            print(er)
            tries = tries +1
            if tries < max_missed_together:
                continue
            else:
                print('Max paginations missed')
                sys.exit(22)
        get_item_data(html)


if __name__ == '__main__':
    main()