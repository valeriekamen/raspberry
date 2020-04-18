#!/usr/bin/env python

import os
import requests
import logging


# Query Bart Departures with Bart api to scrape current Bart data for MacArthur
def get_bart():
    try:
        url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=mcar&key=ZXRM-PLTK-9IBT-DWEI&json=y"
        logging.info("Requesting Bart departures from: {}".format(url))
        r = requests.get(url)
        if r.status_code == 200:
            j = r.json()
            station_data = j['root']['station'][0]['etd']
            try:
                return get_next_departures(station_data)
            except Exception:
                return "--"
    except requests.exceptions.RequestException as e:
        logging.error("Could not get departure times from Bart: {}".format(e))
        pass

    return "?"


def get_all_departures(station_data):
    minutes = []
    for item in station_data:
        estimate = item['estimate']
        for e in estimate:
            direction = e.get('direction')
            color = e.get('color')
            if color in ('YELLOW', 'RED', 'WHITE') and direction == 'South':
                mins = e.get('minutes')
                if not mins == 'Leaving':
                    minutes.append(mins)
    return minutes


def get_next_departures(station_data):
    minutes = get_all_departures(station_data)
    walking_time = 8  # make arg later
    mins_in_walking_time = [m for m in minutes if int(m) - walking_time > 0]
    mins_in_walking_time.sort()
    print(mins_in_walking_time[-2:])
    return mins_in_walking_time[-2:]


if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    get_bart()
