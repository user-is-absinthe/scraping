def csv_line_writer(path, data, separator='\t', encode='utf-16'):
    with open(path, 'a', encoding=encode) as csv_file:
        line = ''
        for index_column in range(len(data)):
            line += str(data[index_column])
            if index_column != len(data) - 1:
                line += separator
        line += '\n'
        csv_file.write(line)
    pass


def csv_data_writer(path, data, separator='\t', encode='utf-16'):
    with open(path, 'a', encoding=encode) as csv_file:
        for line in data:
            now_line = ''
            for index_column in range(len(line)):
                now_line += str(line[index_column])
                if index_column != len(line) - 1:
                    now_line += separator
            now_line += '\n'
            csv_file.write(now_line)
    pass


def csv_reader(path, separator='\t', headline=False, encode='utf-16'):
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


if __name__ == '__main__':
    pass
