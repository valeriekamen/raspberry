import aqi
import logging
import os
import time
import typing
import scrollphat
from datetime import datetime

TEMP_AND_AQI = None

def scroll_message_once():
    length = scrollphat.buffer_len()

    for i in range(length):
        try:
            scrollphat.scroll()
            time.sleep(0.1)
        except KeyboardInterrupt:
            scrollphat.clear()
            raise

def new_weather_or_cache():
    """
    AQI calls their stations once an hour on the hour, but takes ~10 min to show up
    Scrolling takes 6 seconds, checking for second in that interval

    Example response:
    {"status":"success","data":{"city":"San Francisco","state":"California","country":"USA",
    "location":{"type":"Point","coordinates":[-122.3978,37.7658]},
    "current":{"weather":{"ts":"2020-09-05T16:00:00.000Z","tp":20,"pr":1015,"hu":72,"ws":0.55,"wd":181,"ic":"03d"},
    "pollution":{"ts":"2020-09-05T16:00:00.000Z","aqius":93,"mainus":"p2","aqicn":46,"maincn":"p2"}}}}%
    """

    now_min = datetime.now().strftime('%M:%S')
    if now_min >= '15:00' and now_min <= '15:05':
        logging.info('Min is {}, getting new AQI'.format(now_min))    
        new_info = aqi.get_aqi()
        TEMP_AND_AQI['temp'] = new_info['temp']
        TEMP_AND_AQI['aqi'] = new_info['aqi']


if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    scrollphat.set_brightness(4)
    TEMP_AND_AQI = aqi.get_aqi()

    while True:
        try:
            new_weather_or_cache() # check if time for an update
            temp = TEMP_AND_AQI['temp']
            aqilevel = TEMP_AND_AQI['aqi']
            msg = "TEMP {} AQI {} ".format(str(temp), str(aqilevel))
            scrollphat.write_string(msg)
            scroll_message_once()

        except KeyboardInterrupt:
            scrollphat.clear()
            raise
