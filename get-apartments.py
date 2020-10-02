#!/usr/bin/env python3

import re
import os
import requests
import yaml
from bs4 import BeautifulSoup

from generate_numbers import get_numbers

BASE_URL = 'https://nazwa/inwestycje-mieszkaniowe/bienkowice/mieszkanie'

BUILDINGS = ['a1', 'a2', 'a3']
FLORS = [1, 2, 3, 4]
APARTMENT_NUMBERS = range(1, 12)
DECLARED_APARTMENT_COUNT = 96
INVESTMENT_NAME = "Bieńkowice"
STREET_NAME = "Syryjska"

dump_file = '/tmp/dump-file'


def read_file(dump_file):
    if (dump_file and os.path.isfile(dump_file)
            and os.stat(dump_file).st_size != 0):
        with open(dump_file, 'r') as f:
            return f.readlines()

def write_file(urls, f):
    with open(f, 'w') as f:
        for url in urls:
            f.write("%s\n" % url)


def generate_urls(building, flor, apartment, p_id):
    name = "%s-%s-%s" % (building, flor, apartment)
    return "%s:%s,%s" % (BASE_URL, name, p_id)


def get_apartment_state(item, apartment_info, apartment_number):
    if (item.find('span', attrs={'class': 'fright f-green'})
            and item.find('span',
                          attrs={'class': 'fright f-green'}
                          ).text == 'Wolne'):
        state = 'free'

    if (item.find('span', attrs={'class': 'fright f-blue'})
            and item.find('span',
                          attrs={'class': 'fright f-blue'}
                          ).text == 'Zarezerwowane'):
        state = 'reserved'

    if (item.find('span', attrs={'class': 'fright f-red'})
            and item.find('span',
                          attrs={'class': 'fright f-red'}
                          ).text == 'Sprzedane'):
        state = 'sold'

    apartment_info[state][apartment_number] = {}
    apartment_info[state][apartment_number]['url'] = url

    return state, apartment_info


def set_address(apartment_info, mapped_addresses):
    for state in apartment_info:
        for apartment in apartment_info[state]:
            apartment_info[state][apartment] = mapped_addresses.get(apartment,
                                                                    None)

    return apartment_info


def parse_site(url, apartment_info, apartment_temp):
    home = requests.get(url)

    if 'Pobierz kartę mieszkania' not in home.text:
        return

    soup = BeautifulSoup(home.text, 'html.parser')
    for item in soup.find_all('div', attrs={'class': 'col-left'}):
        if (item.find('h2', attrs={'class': 'h666'})
                and item.find('h2', attrs={
                    'class': 'h666'
                }).text != INVESTMENT_NAME):
            continue

        apartment_number = item.find('span', attrs={
            'class': 'th-fake'
        }).text.split()[1]

        if not apartment_number:
            print("Some problem occured during parsing %s" % url)
            return

        if apartment_number not in apartment_temp:
            apartment_temp.append(apartment_number)
        elif apartment_number in apartment_temp:
            print("There is double URLs %s for apartment %s" % (
                url, item.find('span', attrs={'class': 'th-fake'}
                               ).text))

        state, apartment_info = get_apartment_state(item, apartment_info,
                                                    apartment_number)

        fright_class = item.findAll('span',
                                    attrs={'class': 'fright'})
        if not fright_class:
            continue

        for span_class in fright_class:
            if not re.match(r"[0-9]{2},[0-9]{2}", span_class.text):
                continue

            if '+' in span_class.text:
                continue

            apartment_info[state][apartment_number]['size'] = span_class.text
            print("Apartment %s has size: %s" %
                  (url, span_class.text))

        return apartment_info




if __name__ == '__main__':
    #urls = read_file(dump_file)
    #write_to_file = False

    urls = [
     'https://nazwa/inwestycje-mieszkaniowe/bienkowice/mieszkanie:a1-2-1,2094',
     'https://nazwa/inwestycje-mieszkaniowe/bienkowice/mieszkanie:a1-3-4,2103',
     'https://nazwa/inwestycje-mieszkaniowe/bienkowice/mieszkanie:a2-4-6,2615',
     'https://nazwa/inwestycje-mieszkaniowe/bienkowice/mieszkanie:a2-2-3,2185']

    if not urls:
        urls = []
        write_to_file = True
        for building in BUILDINGS:
            for flor in FLORS:
                for apartment in APARTMENT_NUMBERS:
                    for p_id in range(2000, 2300):
                        urls.append(generate_urls(building, flor, apartment, p_id))

    apartment_temp = []
    apartment_info = {'sold': {}, 'free': {}, 'reserved': {}}

    for url in urls:
        apartment_info = parse_site(url, apartment_info, apartment_temp)

    mapped_addresses = get_numbers(STREET_NAME)

    apartment_info = set_address(apartment_info, mapped_addresses)

    with open('apartment_info.yaml', 'w') as f:
        yaml.dump(apartment_info, f)

    #if len(apartment_size) > DECLARED_APARTMENT_COUNT:
    #    print("There are more apartments that it should be!")
