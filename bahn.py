#!/usr/bin/env python3
# coding: utf-8
"""Usage:   bahn.py [<TIME>]
            bahn.py <ORIGIN> <DESTINATION> [<TIME>]
            bahn.py (--preset <PRESET_NAME>)

Shows the departure, arrival and delay of trains.

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
import data
from data import TrainInfoQueryBuilder
from data import DataFetcher
from config import Config


def _print_timetable(origin, destination, timetable):
    for train_info in timetable:
        departure = train_info.departure
        arrival = train_info.arrival
        transportation = train_info.transportation
        print('Origin:', origin, departure.strip(), '|',
              'Destination:', destination, arrival.strip(), transportation)


def _parse_args(args):
    # regular expression for format HH:MM
    time_regex = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if args['<TIME>'] and not re.match(time_regex, args['<TIME>']):
        print('Invalid time format. Use HH:MM')
        sys.exit(1)

if __name__ == "__main__":
    config = Config.load("config/config.json")

    args = docopt(__doc__, version='bahn.py 0.1')
    _parse_args(args)

    default_route = config.default_route
    if args['--preset']:
        preset_name = args['<PRESET_NAME>']
        preset = config.presets.get(preset_name, None)

        if not preset:
            print('There is no preset named', preset_name)
            sys.exit(1)
        origin = preset.origin or default_route.origin
        destination = preset.destination or default_route.destination
        departure_time = preset.departure_time or default_route.departure_time
    else:
        origin = args['<ORIGIN>'] or default_route.origin
        destination = args['<DESTINATION>'] or default_route.destination
        departure_time = args['<TIME>'] or default_route.departure_time

    if not origin or not destination or not departure_time:
        print('Provide the route information and/or set a default route')
        sys.exit(1)

    url = TrainInfoQueryBuilder().with_route(origin, destination).with_departure_time(
        departure_time).include_tram().include_metro().include_regional_train().include_interurban_train().build()

    ignore_ssl = config.network.get('ignore_ssl', False)
    proxies = config.network.get('proxies', {})

    timetable = data.get_timetable(url, proxies, ignore_ssl)
    _print_timetable(origin, destination, timetable)
