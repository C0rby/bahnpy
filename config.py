import json
from model import Route


def _read(path):
    with open(path) as config_file:
        return json.load(config_file)


def _write(config, path):
    with open(path, 'w') as config_file:
        json.dump(config, config_file, indent=4)


def _dict_to_route(route_dict):
    return Route(route_dict.get('origin', ''), route_dict.get('destination', ''), route_dict.get('departure_time', ''))


def _route_to_dict(route):
    return {'origin': route.origin, 'destination': route.destination, 'departure_time': route.departure_time}


class Config:

    def __init__(self, path, config):
        self.path = path
        self.__config = config

    @classmethod
    def load(cls, path):
        config = _read(path)
        return cls(path, config)

    @property
    def proxy(self):
        return self.__config.get('proxy', {})

    @property
    def default_route(self):
        default = self.__config.get('default_route', {})
        return _dict_to_route(default)

    @property
    def presets(self):
        config_presets = self.__config.get('presets', {})
        presets = {}
        for key, preset in config_presets.items():
            presets[key] = _dict_to_route(preset)
        return presets

    def add_preset(self, key, route):
        presets = self.__config.get('presets', {})
        presets[key] = _route_to_dict(route)
        self.__config['presets'] = presets

    def save(self, path=None):
        _write(self.__config, path or self.path)
