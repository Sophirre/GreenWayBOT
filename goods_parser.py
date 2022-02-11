#!/usr/bin/env python3

import socket

from requests import get
from json import dump, load
from schedule import every, run_pending
from time import sleep, strftime, localtime

URLS = {
    'special_offers': 'https://pyapi.greenwaystart.com/pyapi/v1/greenway/shop/section/all/',
    'textile': 'https://pyapi.greenwaystart.com/pyapi/v1/greenway/shop/section/textile/',
    'house': 'https://pyapi.greenwaystart.com/pyapi/v1/greenway/shop/section/house/'
}


def json_get(section):
    url = URLS[section]
    r = get(url)
    if r.status_code != 200:
        return print(r.status_code)
    return r.json()


def json_file_create(section):
    my_json = json_get(section)
    with open(f'./json/data/{section}.json', 'w') as f:
        dump(my_json, f, indent=4, ensure_ascii=False)


def json_file_update():
    print(strftime("%H:%M:%S", localtime(),))
    keys = URLS.keys()
    for key in keys:
        print(key)
        collect_data(key)


def collect_data(section):
    my_json = json_get(section)
    result_list = []
    products = my_json.get('products')
    i = -1
    for product in products:
        i +=1
        if product.get('stock_product').get('discount') != 0:
            print(i, product.get('name'))
        try:
            result_list.append(
                {
                    'id': product.get('id'),
                    'name': product.get('name'),
                    'price': product.get('stock_product').get('price'),
                    'without_discount': product.get('stock_product').get('old_price'),
                    'discount': product.get('stock_product').get('discount'),
                    'can_order': product.get('stock_product').get('can_order'),
                    'image': product.get('image').get('origin').get('path'),

                }
            )
        except AttributeError as e:
            print(e)
            result_list.append(
                {
                    'id': product.get('id'),
                    'name': product.get('name'),
                    'price': product.get('stock_product').get('price'),
                    'without_discount': product.get('stock_product').get('old_price'),
                    'discount': product.get('stock_product').get('discount'),
                    'can_order': product.get('stock_product').get('can_order'),
                    'image': None

                }
            )
    with open(f'json/data/{section}.json', 'w') as j:
        dump(result_list, j, indent=4, ensure_ascii=False)


def connection_check():
    try:
        socket.gethostbyaddr('1.1.1.1')
    except socket.herror:
        return False
    return True


def main():
    print(strftime("%H:%M:%S", localtime()))
    every(30).minutes.do(json_file_update)
    while 1:
        if connection_check():
            run_pending()
            sleep(1)
        else:
            continue


if __name__ == '__main__':
    main()

