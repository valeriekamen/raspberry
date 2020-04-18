#!/usr/bin/env python

import os
import requests
import typing
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class BartDepartures():
    def __init__(self, station: str = 'mcar',
                 walking_time: int = 8,
                 number_of_trains: int = 2,
                 direction: str = 'South',
                 only_sf_bound: bool = True,
                 debug: bool = False) -> None:
        self.station = station  # List of statation codes: https://api.bart.gov/docs/overview/abbrev.aspx
        self.walking_time = walking_time  # Time in minutes until you can be at the station
        self.number_of_trains = number_of_trains  # How many train arrival times to show
        self.direction = direction  # North or South only
        self.only_sf_bound = only_sf_bound  # certain colors on SF track
        self.debug = debug

    def get_bart(self):
        try:
            url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&key=ZXRM-PLTK-9IBT-DWEI&json=y".format(self.station)
            logging.info("Requesting Bart departures from: {}".format(url))
            r = requests.get(url)
            if self.debug:
                print(url)
            if r.status_code == 200:
                j = r.json()
                station_data = j['root']['station'][0]['etd']
                try:
                    return self.get_next_departures(station_data)
                except Exception:
                    return "--"
        except requests.exceptions.RequestException as e:
            logging.error("Could not get departure times from Bart: {}".format(e))
            pass

        return

    def get_all_departures(self, station_data):
        mins_with_colors = []
        for item in station_data:
            estimate = item['estimate']
            for e in estimate:
                color = e.get('color')
                if e.get('direction') == self.direction:
                    mins = e.get('minutes')
                    if not mins == 'Leaving':
                        train = {}
                        train['color'] = color
                        train['mins'] = e.get('minutes')
                        mins_with_colors.append(train)

        if self.debug:
            print(mins_with_colors)

        logging.info('Found {} trains in right direction'.format(len(mins_with_colors)))

        if self.only_sf_bound:
            return self.make_list_of_trains_sf_only(mins_with_colors)

        return self.make_list_of_trains(mins_with_colors)

    @staticmethod
    def make_list_of_trains_sf_only(mins_with_colors: typing.List):
        return [item.get('mins') for item in mins_with_colors if item.get('color') in ('YELLOW', 'RED', 'WHITE')]

    @staticmethod
    def make_list_of_trains(mins_with_colors: typing.List):
        return [item.get('mins') for item in mins_with_colors]

    def get_next_departures(self, station_data):
        minutes = self.get_all_departures(station_data)
        if self.debug:
            print('walking time:', self.walking_time,
                  'number of trains:', self.number_of_trains)
        mins_in_walking_time = [m for m in minutes if int(m) - self.walking_time > 0]
        logging.info('Trains in walking time: {}'.format(len(mins_in_walking_time)))
        mins_in_walking_time.sort()
        if len(mins_in_walking_time) < self.number_of_trains:
            return mins_in_walking_time
        else:
            return mins_in_walking_time[:self.number_of_trains]
