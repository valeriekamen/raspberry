import os
import re
import logging
from bs4 import BeautifulSoup
import requests


def get_weather():
    weather = {}
    try:
        coords = '37.80508000000003,-122.27306999999996'  # 3906 Ruby, Oakland CA
        url = "https://darksky.net/forecast/{}/uk212/en".format(coords)
        logging.info("Requesting weather from: {}".format(url))
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "lxml")
            weather['summary'] = soup.find("span", "summary").text
            weather['feelslike'] = make_farenheit(soup.find("span", "feels-like-text").text)
            weather['high'] = make_farenheit(soup.find("span", "high-temp-text").text)
            weather['low'] = make_farenheit(soup.find("span", "low-temp-text").text)
    except requests.exceptions.RequestException as e:
        logging.error("Could not get weather data from DarkSky: {}".format(e))
        pass

    return weather


def make_farenheit(temp):
    t = re.sub("[^0-9]", "", temp)
    return str(int((9 * int(t))/5 + 32))


if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    weather = get_weather()
    print(weather)
