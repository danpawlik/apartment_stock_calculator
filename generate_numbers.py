#!/usr/bin/env python3

budynek = ['A1', 'A2', 'A3']
kondygnacja = list(range(1,5))
numer = list(range(1,10))
base_name = "Ulica "

def get_budynek_number(b, nr):
    if b == 'A1':
        if nr <= 3:
            budynek_id = 2
        elif nr > 3 and nr <= 6:
            budynek_id = 4
        elif nr >= 7:
            budynek_id = 'brak'
    if b == 'A2':
        if nr <= 3:
            budynek_id = 6
        elif nr > 3 and nr <= 6:
            budynek_id = 8
        elif nr >= 7:
            budynek_id = 10
    if b == 'A3':
        if nr <= 3:
            budynek_id = 12
        elif nr > 3 and nr <= 6:
            budynek_id = 14
        elif nr >= 7:
            budynek_id = 16

    return budynek_id

def get_apartment_number(k, nr):
    n_mieszkania = ''
    if k == 1:
        if nr == 1 or nr == 4 or nr == 7:
            n_mieszkania = 1
        if nr == 2 or nr == 5 or nr == 8:
            n_mieszkania = 2
        if nr == 3 or nr == 6 or nr == 9:
            n_mieszkania = 3
    elif k == 2:
        if nr == 1 or nr == 4 or nr == 7:
            n_mieszkania = 4
        if nr == 2 or nr == 5 or nr == 8:
            n_mieszkania = 5
        if nr == 3 or nr == 6 or nr == 9:
            n_mieszkania = 6
    elif k == 3:
        if nr == 1 or nr == 4 or nr == 7:
            n_mieszkania = 7
        if nr == 2 or nr == 5 or nr == 8:
            n_mieszkania = 8
        if nr == 3 or nr == 6 or nr == 9:
            n_mieszkania = 9
    elif k == 4:
        if nr == 1 or nr == 4 or nr == 7:
            n_mieszkania = 10
        if nr == 2 or nr == 5 or nr == 8:
            n_mieszkania = 11
        if nr == 3 or nr == 6 or nr == 9:
            n_mieszkania = 12

    return n_mieszkania

def get_numbers(base_name):
    numeracja = {}
    for b in budynek:
        for k in kondygnacja:
            for nr in numer:
                nazwa = "%s.%s.%s" % (b, k, nr)
                budynek_id = get_budynek_number(b, nr)
                nr_mieszkania = get_apartment_number(k, nr)

                if not nr_mieszkania:
                    continue

                if not budynek_id:
                    continue

                numeracja[nazwa] = "%s %s/%s" % (base_name, budynek_id,
                                                 nr_mieszkania)
    return numeracja

if __name__ == '__main__':
    print(get_numbers())
