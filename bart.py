#!/usr/bin/env python

import os
import requests
import typing
import logging
from enum import Enum
from collections import namedtuple

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class Direction(Enum):
    NORTH = 'North'
    SOUTH = 'South'


class Colors(Enum):
    YELLOW = 'YELLOW'
    RED = 'RED'
    WHITE = 'WHITE'
    ORANGE = 'ORANGE'


Estimate = namedtuple('Estimate', ['color', 'direction', 'mins'])

test_json = '''
{
  "?xml": {
    "@version": "1.0",
    "@encoding": "utf-8"
  },
  "root": {
    "@id": "1",
    "uri": {
      "#cdata-section": "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=mcar&json=y"
    },
    "date": "04/18/2020",
    "time": "04:15:31 PM PDT",
    "station": [
      {
        "name": "MacArthur",
        "abbr": "MCAR",
        "etd": [
          {
            "destination": "Antioch",
            "abbreviation": "ANTC",
            "limited": "0",
            "estimate": [
              {
                "minutes": "2",
                "platform": "3",
                "direction": "North",
                "length": "10",
                "color": "YELLOW",
                "hexcolor": "#ffff33",
                "bikeflag": "1",
                "delay": "0"
              },
              {
                "minutes": "22",
                "platform": "3",
                "direction": "North",
                "length": "10",
                "color": "YELLOW",
                "hexcolor": "#ffff33",
                "bikeflag": "1",
                "delay": "0"
              },
              {
                "minutes": "42",
                "platform": "3",
                "direction": "North",
                "length": "10",
                "color": "YELLOW",
                "hexcolor": "#ffff33",
                "bikeflag": "1",
                "delay": "0"
              }
            ]
          }
        ]
      }
    ],
    "message": ""
  }
}
'''

SF_BOUND_COLORS = (Colors.YELLOW, Colors.RED, Colors.WHITE)
HOME_BOUND_COLORS = (Colors.YELLOW)  # todo more colors


class StationData:
    def __init__(self, station_data):
        self.estimates = []
        for destination in station_data:
            for estimate in destination['estimate']:
                if not estimate['minutes'] == 'Leaving':
                    self.estimates.append(Estimate(color=Colors(estimate['color']), mins=int(
                        estimate['minutes']), direction=Direction(estimate['direction'])))

    def get_by_colors_and_direction(self, colors: typing.List[Colors],  direction: Direction) -> typing.List[Estimate]:
        estimates = [e for e in self.estimates if e.direction == direction and e.color in colors]

        return sorted(estimates, key=lambda e: e.mins)


class BartDepartures:
    def __init__(self,
                 api_key: str,
                 station: str) -> None:
        self.api_key = api_key
        self.station = station  # List of statation codes: https://api.bart.gov/docs/overview/abbrev.aspx
        self.url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig={station}&key={api_key}&json=y".format(
            station=self.station, api_key=self.api_key)

    def get_station_data(self) -> StationData:
        try:
            logging.info("Requesting Bart departures from: {}".format(self.url))
            r = requests.get(self.url)
            if r.status_code == 200:
                return StationData(r.json()['root']['station'][0]['etd'])
        except Exception as e:
            logging.error("Could not get departure times from Bart: {}".format(e))
            pass
