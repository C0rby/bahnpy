# coding: utf-8


import urllib.parse
import requests
from bs4 import BeautifulSoup
from collections import namedtuple


TrainInfo = namedtuple('TrainInfo', 'departure arrival transportation')

class TrainInfoQueryBuilder(object):
    __base_url = 'https://reiseauskunft.bahn.de/bin/query.exe/dn?'

    def __init__(self):
        # Start the search immediatly
        self.params = {'start': '1'}

    def with_route(self, start, destination):
        start_key = 'S'
        destination_key = 'Z'
        self.params[start_key] = start
        self.params[destination_key] = destination
        return self

    def with_departure_time(self, time):
        self.params['time'] = time
        return self

    def include_regional_train(self):
        self.params['REQ0JourneyProduct_prod_section_0_3'] = '1'
        return self

    def include_interurban_train(self):
        self.params['REQ0JourneyProduct_prod_section_0_4'] = '1'
        return self

    def include_metro(self):
        self.params['REQ0JourneyProduct_prod_section_0_7'] = '1'
        return self

    def include_tram(self):
        self.params['REQ0JourneyProduct_prod_section_0_8'] = '1'
        return self

    def build(self):
        return self.__base_url + urllib.parse.urlencode(self.params)


class DataFetcher(object):

    def __init__(self, proxies=None, ignore_ssl=False):
        self.proxies = proxies
        self.ignore_ssl = ignore_ssl

        if(ignore_ssl):
            requests.packages.urllib3.disable_warnings()  # disable ssl warning

    def fetch_data(self, url):
        return requests.get(url, proxies=self.proxies, verify=not self.ignore_ssl)

def _soup(content):
    return BeautifulSoup(content, 'html.parser')


def create_timetable(response_html):
    response = _soup(response_html)
    table_top_rows = response('tr', 'firstrow')
    table_bottom_rows = response('tr', 'last')

    times = []
    for top_row, bottom_row in zip(table_top_rows, table_bottom_rows):
        departure = get_time(top_row)
        arrival = get_time(bottom_row)
        means_of_transportation = get_means_of_transportion(top_row)
        times.append(TrainInfo(departure, arrival, means_of_transportation))
    return times


def get_means_of_transportion(row_html):
    row = _soup(str(row_html))
    means_of_transportation = row('td', 'products')
    return 'N/A' if not means_of_transportation else means_of_transportation[0].get_text().replace('\n', '')


def get_time(row_html):
    row = _soup(str(row_html))
    return row('td', 'time')[0].get_text().replace('\n', '')

def get_timetable(url, proxies=None, ignore_ssl=False):
    fetcher = DataFetcher(proxies, ignore_ssl)

    response = fetcher.fetch_data(url)
    return create_timetable(response.text)
