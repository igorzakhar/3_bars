import os
import re
import json
import math
import argparse
import zipfile

import requests


def get_remote_file():
    url = 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=84505'
    response = requests.get(url)
    return response.content, response.headers


def save_file(content, headers):
    attachment = headers['Content-Disposition']
    filename = re.findall("filename=(.+)", attachment)[0]
    attachment_filename = re.sub('"', '', filename)
    with open(attachment_filename, 'wb') as file:
        file.write(content)
    return attachment_filename


def unzip_file(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    return zip_ref.namelist()[0]


def load_data(filename, content_encoding):
    with open(filename, 'r', encoding=content_encoding) as file:
        json_data = json.load(file)
    return json_data


def get_biggest_bar(data):
    biggest_bar = max(data, key=lambda item: item['SeatsCount'])
    return biggest_bar


def get_smallest_bar(data):
    smallest_bar = min(data, key=lambda item: item['SeatsCount'])
    return smallest_bar


def get_distance(data, latitude, longitude):
    y_square = (latitude - data['geoData']['coordinates'][0]) ** 2
    x_square = (longitude - data['geoData']['coordinates'][1]) ** 2
    distance = math.sqrt(y_square + x_square)
    return distance


def get_user_coordinate():
    message = "Type your coordinates (latitude longitude) with a space delimiter: "
    latitude, longitude = [float(item) for item in input(message).split() ]
    return latitude, longitude

def get_closest_bar(data, latitude, longitude):
    distance = lambda data_item: get_distance(data_item, latitude, longitude)
    #lst = [get_distance(item_data, latitude, longitude) for item_data in data]
    closest_bar = min(data, key=distance)
    return closest_bar

def process_args():
    parser = argparse.ArgumentParser("Get the closest bar to user coordinates")
    parser.add_argument('-c', '--closest', action='store_true', 
                        help='Your coordinates: latitude longitude')
    return parser.parse_args()

if __name__ == '__main__':
    args = process_args()
    content, headers = get_remote_file()
    zip_file = save_file(content, headers)
    unzip_filename = unzip_file(zip_file)
    content_encoding = headers['Content-Encoding']
    json_data = load_data(unzip_filename, content_encoding)
    smallest_bar = get_smallest_bar(json_data)
    biggest_bar = get_biggest_bar(json_data)
    print("The biggest bar: {}, {} seats".format(biggest_bar['Name'], 
                                           biggest_bar['SeatsCount']))
    print("The smallest bar: {}, {} seats".format(smallest_bar['Name'],
                                                  smallest_bar['SeatsCount']))
    if args.closest:
        latitude, longitude = get_user_coordinate()
        closest_bar = get_closest_bar(json_data, latitude, longitude)
        print('-------/Closest Bar/-------')
        print('Name: {}\nAddress: {}'.format(closest_bar['Name'], 
                                         closest_bar['Address'] ))




