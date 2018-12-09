import os

import my_csv


PATH_TEMP_PHOTOS_LINKS = 'data/temp'


def get_photos():
    pass


def main():
    global PATH_TEMP_PHOTOS_LINKS
    all_photos = list()
    while True:
        files = os.listdir(PATH_TEMP_PHOTOS_LINKS)
        # user_photos = list()
        for csv in files:
            user_photos = my_csv.csv_reader(PATH_TEMP_PHOTOS_LINKS + '/' + csv, separator='\t')
            # for


    pass


if __name__ == '__main__':
    main()
