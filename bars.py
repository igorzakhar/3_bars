import os
import re
import json
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
    pass


def get_smallest_bar(data):
    pass


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    content, headers = get_remote_file()
    zip_file = save_file(content, headers)
    unzip_filename = unzip_file(zip_file)
    content_encoding = headers['Content-Encoding']
    json_data = load_data(unzip_filename, content_encoding)
    print(json_data)


