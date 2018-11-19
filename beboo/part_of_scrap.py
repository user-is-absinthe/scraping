from datetime import datetime


PATH_TO_LOG = 'data/beboo.log'
# PATH_TO_USERS_LINKS = 'data/users_links.csv'
PATH_TO_USERS_LINKS = 'data/users_links_100.csv'
PATH_TO_USERS_INFORMATION = 'data/users.csv'
PATH_TO_PHOTOS_LINKS = 'data/photos_links.csv'
PATH_TO_PHOTOS = 'data/photos'


def csv_reader(path, separator, headline=False, encode='utf-16'):
    with open(path, 'r', encoding=encode) as file:
        csv_file = file.readlines()
    csv_file = [this.strip() for this in csv_file]
    if headline:
        keys_to_dict = csv_file[0].split(separator)
    else:
        keys_to_dict = [i for i in range(0, len(csv_file[0].split(separator)))]

    opened_csv = dict()
    for key in keys_to_dict:
        opened_csv[key] = list()

    for line in csv_file:
        if headline and line == csv_file[0]:
            continue
        separated_line = line.split(separator)
        for index in range(len(keys_to_dict)):
            opened_csv[keys_to_dict[index]].append(separated_line[index])

    return opened_csv


def csv_line_writer(path, data, separator='\t', encode='utf-16'):
    csv_file = open(path, 'a', encoding=encode)
    line = ''
    for column in data:
        line += str(column)
        if column != data[-1]:
            line += separator
    line += '\n'
    csv_file.write(line)
    csv_file.close()


def write_csv_head():
    csv_line_writer(PATH_TO_USERS_INFORMATION,
                    [
                        'id_user', 'link_to_user', 'имя', 'пол', 'тип аккаунта', 'возраст', 'страна',
                        'город', 'о себе', 'кого ищет', 'семейное положение', 'доход', 'материальное положение',
                        'проживание', 'наличие автомобиля', 'отношение к курению', 'отношение к алкоголю',
                        'знание языков',
                        'рост, см', 'вес, кг', 'цвет волос', 'цвет глаз', 'телосложение', 'татуировки', 'пирсинг',
                        'волосы на лице и на теле', 'ориентация', 'тип секса', 'роль', 'позы', 'действия',
                        'эрогенные зоны',
                        'фетиши'
                    ]
                    )
    csv_line_writer(PATH_TO_PHOTOS_LINKS, ['id_user', 'link_to_photo'])
    information('CSV head created successful.')


def information(info):
    to_write = '[' + datetime.now().strftime("%B %d %Y, %H:%M:%S") + ']\t' + info + '\n'
    print(to_write)
    with open(PATH_TO_LOG, 'a') as file:
        file.write(to_write)
    pass


def load_user_links():
    user_links = csv_reader(path=PATH_TO_USERS_LINKS, separator='\t', headline=True, encode='ansi')
    user_links = user_links['link_to_user']
    information('User links load successful.')
    return user_links


def main():
    # print(csv_reader(path='data/users_links_100.csv', separator='\t', headr=True, encode='ansi'))
    # csv_writer_line(path='test.csv', data=['dawdaw', 123, None], encode='ansi')
    information('Start program.')
    user_links = load_user_links()

    pass


if __name__ == '__main__':
    main()
