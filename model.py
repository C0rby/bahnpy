class Route(object):

    def __init__(self, origin='', destination='', departure_time=''):
        self.__origin = origin
        self.__destination = destination
        self.__departure_time = departure_time

    @property
    def origin(self):
        return self.__origin

    @property
    def destination(self):
        return self.__destination

    @property
    def departure_time(self):
        return self.__departure_time
