#!/usr/bin/env python3

import re
import os
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.DEVELOPER/inwestycje-mieszkaniowe/bienkowice/mieszkanie'

BUILDINGS = ['a1', 'a2', 'a3']
FLORS = [1, 2, 3, 4]
APARTMENT_NUMBERS = range(1, 12)
DECLARED_APARTMENT_COUNT = 96
INVESTMENT_NAME = "Bieńkowice"

apartment_size = {}
apartment_temp = []
reserved = []
free = []

urls = []

dump_file = '/tmp/dump-file'
apartment_size_file = '/tmp/apartment_size'

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

def parse_site(url):
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

        if (item.find('span', attrs={'class': 'fright f-green'})
                and item.find('span',
                              attrs={'class': 'fright f-green'}
                              ).text == 'Wolne'):
            free.append(url)

        if (item.find('span', attrs={'class': 'fright f-blue'})
                and item.find('span',
                              attrs={'class': 'fright f-blue'}
                              ).text == 'Zarezerwowane'):
            reserved.append(url)

        if not item.findAll('span',
                            attrs={'class': 'fright f-red'}):
            continue

        if (item.find('span', attrs={'class': 'th-fake'}).text
                not in apartment_temp):
            apartment_temp.append(item.find(
                'span', attrs={'class': 'th-fake'}))
        elif (item.find('span', attrs={'class': 'th-fake'}).text
                in apartment_temp):
            print("There is double URLs %s for apartment %s" % (
                url, item.find('span', attrs={'class': 'th-fake'}
                               ).text))

        fright_class = item.findAll('span',
                                    attrs={'class': 'fright'})
        if not fright_class:
            continue
        for span_class in fright_class:
            if not re.match(r"[0-9]{2},[0-9]{2}", span_class.text):
                continue

            if '+' in span_class.text:
                continue

            name = item.find('span', attrs={'class': 'th-fake'}
                             ).text.split()[1]
            apartment_size[name] = span_class.text
            print("Apartment %s has size: %s" %
                  (url, span_class.text))

            return url


urls = read_file(dump_file)
write_to_file = False

if not urls:
    urls = []
    write_to_file = True
    for building in BUILDINGS:
        for flor in FLORS:
            for apartment in APARTMENT_NUMBERS:
                for p_id in range(2000, 2300):
                    urls.append(generate_urls(building, flor, apartment, p_id))

location_urls = []
for url in urls:
    location_urls.append(parse_site(url))

if write_to_file:
    write_file(urls, dump_file)

write_file(apartment_size, apartment_size_file)

if len(apartment_size) > DECLARED_APARTMENT_COUNT:
    print("There are more apartments that it should be!")
