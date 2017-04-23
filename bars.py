import json


def load_data(filepath):
    with open(filepath, 'r', encoding='cp1251') as file:
        json_data = json.load(file)
    return json_data

def get_biggest_bar(data):
    pass


def get_smallest_bar(data):
    pass


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    pass
