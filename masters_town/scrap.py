import requests
from bs4 import BeautifulSoup

#https://www.livemaster.ru/catalogue/suveniry-i-podarki
#40 elements on pages
#https://www.livemaster.ru/catalogue/suveniry-i-podarki?from=40000

#global var
mainpage = 'https://www.livemaster.ru/'
id_item = 0

def get_html(url):
    r=requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find_all('a', class_='pagebar__page')[-1].get('href')  #last page
    total_pages=pages.split('=')[3]
    return int(total_pages)

def img_donwload(url, index):
    name_img = './images/' + str(id_item) + '_' + str(index) + '.jpg'
    f = open(name_img, 'wb')
    f.write(requests.get(url).content)
    f.close()

def write_comment(data):
    file_name='./data/comments'
    try:
        file_to_csv = open(file_name + '.csv', 'a', encoding='UTF-16')
    except FileNotFoundError:
        file_to_csv = open(file_name + '.csv', 'w', encoding='UTF-16')

    file_to_csv.write(
        data['id'] + '; ' + data['title'] + '; ' + data['name'] + ';' + data['comment'] + '\n'
    )
    print('comment csv success!' + data['id'])
    file_to_csv.close()

def write_csv(data):
    # with open('./data/livemasters.csv', 'w') as f:
    #     writer = csv.writer(f, delimiter=' ',
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(
    #         data[0]['id_item'],
    #         # data['title'],
    #         # data['price'],
    #         # data['description'],
    #         # data['recomend'],
    #         # data['return_']
    #     )
    file_name = './data/items_list'
    try:
        file_to_csv = open(file_name + '.csv', 'a', encoding='UTF-16')
    except FileNotFoundError:
        file_to_csv = open(file_name + '.csv', 'w', encoding='UTF-16')

    file_to_csv.write(
        data['id_item'] + '; ' + data['title'] + '; ' + data['price'] + '; ' + data['description'] + '; ' + data['recomend'] + '; ' + data['return_'] + ';' + data['url']+'\n'
    )
    print('\nTo csv success! New item №' + data['id_item'])
    file_to_csv.close()


def get_item_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('a', class_='item-block__name')
    #id_item = 0
    for item in items:
        global mainpage
        item_url = mainpage + item.get('href')
        print(item_url)
        item_soup = BeautifulSoup(get_html(item_url), 'lxml')
        global id_item
        id_item = id_item + 1
        photos = item_soup.find_all('a', class_ = 'photo-switcher__largephoto')
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

        id_item_str = str(id_item)
        item_url_str = str(item_url)
        data = {'id_item' : id_item_str,
                'title' : title,
                'price' : price,
                'description' : description,
                'recomend' : recomend,
                'return_' : return_,
                'url' : item_url_str}

        print(data)
        write_csv(data)

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
                    name = names[j].text.replace('\n','').replace(',','').replace('\t','').replace('\r','').replace('"','').replace('\\U','').replace(';','')
                except IndexError:
                    name = 'Null'
                j = j + 1
                data_coment = {'id' : id_item_str,
                               'title': title,
                               'name' : name,
                               'comment' : comment}
                write_comment(data_coment)

def main():
    base_url = 'https://www.livemaster.ru/catalogue/suveniry-i-podarki?from='
    total_pages = get_total_pages(get_html(base_url))
    for i in range (0, total_pages + 40, 40): #to all pages
    #for i in range(0, 40, 40): #for test
        url_gen = base_url + str(i)
        get_html(url_gen)
        get_item_data(url_gen)


if __name__ == '__main__':
    main()