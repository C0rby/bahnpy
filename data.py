# coding: utf-8


import urllib.parse
import requests
from bs4 import BeautifulSoup


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

    def with_departure_time_at(self, time):
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

    def fetch_data(url):
        return requests.get(url, proxies=self.proxies, verify= !self.ignore_ssl)
