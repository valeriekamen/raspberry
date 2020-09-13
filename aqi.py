import os
import re
import logging
import requests

AQI_KEY = '83d1adcd-5400-4915-9bd3-479da522a4e4'

def get_aqi():
    result = {}
    payload = {}
    headers = {}
    files = {}
    try:
        url = 'http://api.airvisual.com/v2/city?city=San%20Francisco&state=California&country=USA&key={}'.format(AQI_KEY)
        res = requests.request("GET", url, headers=headers, data = payload, files = files)
        logging.info("Requesting AQI info from: {}".format(url))
        if res.status_code == 200:
            data = res.json()
            temp = data['data']['current']['weather']['tp']
            result['temp'] = make_farenheit(temp)
            result['aqi'] = data['data']['current']['pollution']['aqius']

    except requests.exceptions.RequestException as e:
        logging.error("Could not get data from AQIAir: {}".format(e))
        pass

    return result


def make_farenheit(temp):
    return str(int((9 * int(temp))/5 + 32))


if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    get_aqi()
