#!/usr/bin/env python
"""Usage:   bahn.py [<TIME>]
            bahn.py <START> <DESTINATION> [<TIME>]

Shows the departure, arrival and delay of trains.
The default TIME is the 17:42
The default START is "Ostring, Nürnberg"
The default DESTINATION is "Fürth(Bay)Hbf"

Arguments:
  TIME        optional departure time
  START DESTINATION  shows the departure and arrival times from a given START and DESTINATION optional with departure TIME

Options:
  -h --help
  --version
"""

import requests
import urllib.parse  # urllib for python2 or urllip.parse for python3
import re
import sys
from docopt import docopt
from bs4 import BeautifulSoup

default_start = ''
default_destination = ''
default_time = ''

http_proxy = ''
https_proxy = http_proxy
proxies = {'http': http_proxy, 'https': https_proxy}


def fetch_data(start=default_start, destination=default_destination, time=default_time):
    class QueryBuilder(object):
        __base_url = 'https://reiseauskunft.bahn.de/bin/query.exe/dn?'
        __start_param = '&start=1'
        __rbahn_param = '&REQ0JourneyProduct_prod_section_0_3=1'
        __sbahn_param = '&REQ0JourneyProduct_prod_section_0_4=1'
        __ubahn_param = '&REQ0JourneyProduct_prod_section_0_7=1'
        __tram_param = '&REQ0JourneyProduct_prod_section_0_8=1'
        __params = {'start': '1',
                    'REQ0JourneyProduct_prod_section_0_3': '1',
                    'REQ0JourneyProduct_prod_section_0_4': '1',
                    'REQ0JourneyProduct_prod_section_0_7': '1',
                    'REQ0JourneyProduct_prod_section_0_8': '1'
                    }

        def __init__(self):
            pass

        def query(self, start, destination):
            start_key = 'S'
            destination_key = 'Z'
            self.__params[start_key] = start
            self.__params[destination_key] = destination
            return self

        def start_time(self, time):
            time_key = 'time'
            self.__params[time_key] = time
            return self

        def build(self):
            return self.__base_url + urllib.parse.urlencode(self.__params)

    url = QueryBuilder().query(start, destination).start_time(time).build()
    return requests.get(url, proxies=proxies, verify=False)


def soup(content):
    return BeautifulSoup(content, 'html.parser')


def create_times_and_transport(main_content):
    table_top_rows = main_content('tr', 'firstrow')
    table_bottom_rows = main_content('tr', 'last')

    times = []
    for top, bottom in zip(table_top_rows, table_bottom_rows):
        start = get_time(top)
        end = get_time(bottom)
        transport = get_transport(top)
        times.append((start, end, transport))
    return times

def get_transport(row):
    row_soup = soup(str(row))
    products = row_soup('td', 'products')
    return 'N/A' if not products else products[0].get_text().replace('\n', '')

def get_time(row):
    row_soup = soup(str(row))
    return row_soup('td', 'time')[0].get_text().replace('\n', '')


def print_information(start, destination, times):
    for start_time, end, transport in times:
        print('Start:', start, start_time.strip(),'|', 'Ziel:', destination, end.strip(), transport)


def parse_args(args):
    # regular expression for format HH:MM
    time_regex = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if args['<TIME>'] and not re.match(time_regex, args['<TIME>']):
        print('Invalid time format. Use HH:MM')
        sys.exit(0)

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()  # disable ssl warning

    args = docopt(__doc__, version='bahn.py 0.1')
    parse_args(args)

    start = args['<START>'] if args['<START>'] else default_start
    destination = args['<DESTINATION>'] if args[
        '<DESTINATION>'] else default_destination
    time = args['<TIME>'] if args['<TIME>'] else default_time

    response = fetch_data(start, destination, time)
    main_content = soup(response.text)

    times_transport = create_times_and_transport(main_content)
    print_information(start, destination, times_transport)
