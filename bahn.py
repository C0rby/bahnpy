#!/usr/bin/env python
# coding: utf-8
"""Usage:   bahn.py [<TIME>]
            bahn.py <START> <DESTINATION> [<TIME>]

Shows the departure, arrival and delay of trains.
The default TIME is the 17:42
The default START is "Ostring, Nuernberg"
The default DESTINATION is "Fuerth(Bay)Hbf"

Arguments:
  TIME        optional departure time
  START DESTINATION  shows the departure and arrival times from a given START and DESTINATION optional with departure TIME

Options:
  -h --help
  --version
"""

import re
import sys
from docopt import docopt
import requests
from bs4 import BeautifulSoup
from data import TrainInfoQueryBuilder

default_start = 'Nürnberg Ostring'
default_destination = 'Fürth(Bay)Hbf'
default_time = '17:42'

http_proxy = ''
https_proxy = http_proxy
proxies = {'http': http_proxy, 'https': https_proxy}


def fetch_data(start=default_start, destination=default_destination, time=default_time):
    url = TrainInfoQueryBuilder().with_route(start, destination).with_departure_time_at(
        time).include_tram().include_metro().include_interurban_train().include_regional_train().build()
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
        print('Start:', start, start_time.strip(), '|',
              'Ziel:', destination, end.strip(), transport)


def parse_args(args):
    # regular expression for format HH:MM
    time_regex = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if args['<TIME>'] and not re.match(time_regex, args['<TIME>']):
        print('Invalid time format. Use HH:MM')
        sys.exit(0)

if __name__ == "__main__":
    # requests.packages.urllib3.disable_warnings()  # disable ssl warning

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
