# coding: utf-8

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
