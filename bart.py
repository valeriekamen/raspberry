#!/usr/bin/env python

import os
import requests
import logging


# Query Bart Departures with Bart api to scrape current Bart data for MacArthur
def get_bart():
    bart_data = {}
    try:
        url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=mcar&key=ZXRM-PLTK-9IBT-DWEI&json=y"
        logging.info("Requesting Bart departures from: {}".format(url))
        r = requests.get(url)
        if r.status_code == 200:
            j = r.json()
            station_data = j['root']['station'][0]['etd']
            try:
                return get_next_sf_arrival(station_data)
            except Exception:
                return "--"
    except requests.exceptions.RequestException as e:
        logging.error("Could not get departure times from Bart: {}".format(e))
        pass

    return bart_data


def get_next_sf_arrival(station_data):
    minutes = []
    for item in station_data:
        estimate = item['estimate']
        for e in estimate:
            direction = e.get('direction')
            color = e.get('color')
            print(direction, color)
            if color in ('YELLOW', 'RED', 'WHITE') and direction == 'South':
                minutes.append(e.get('minutes'))
    return max(minutes)


if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    get_bart()
