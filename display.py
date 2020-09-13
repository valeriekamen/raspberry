import bart
import weather
import logging
import os
import time
import typing
import scrollphat


def scroll_message_once():
    length = scrollphat.buffer_len()

    for i in range(length):
        try:
            scrollphat.scroll()
            time.sleep(0.1)
        except KeyboardInterrupt:
            scrollphat.clear()
            raise


def filter_bart_departures(estimates: typing.List[bart.Estimate], walking_time: int, max_trains: int):
    mins_in_walking_time = [str(e.mins) for e in estimates if e.mins > walking_time]
    print(mins_in_walking_time)
    logging.info('Trains in walking time: {}'.format(len(mins_in_walking_time)))
    return mins_in_walking_time[:max_trains]


API_KEY = 'ZXRM-PLTK-9IBT-DWEI'
WALKING_TIME = 8
MAX_TRAINS = 2
if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    scrollphat.set_brightness(4)
    current_weather = weather.get_weather()
    feelslike = "{}".format(current_weather.get('feelslike'))
    mcar_station = bart.BartDepartures(api_key=API_KEY, station='mcar')  # defaults for Val home, 2 trains to SF

    while True:
        try:
            station_data = mcar_station.get_station_data()
            estimates = station_data.get_by_colors_and_direction(bart.SF_BOUND_COLORS, bart.Direction.SOUTH)
            print(estimates)
            next_barts_str = ' & '.join(filter_bart_departures(
                estimates=estimates, walking_time=WALKING_TIME, max_trains=MAX_TRAINS))
            msg = "Its {}. Bart in {}  ".format(feelslike, next_barts_str)
            scrollphat.write_string(msg)
            scroll_message_once()
        except KeyboardInterrupt:
            scrollphat.clear()
            raise
