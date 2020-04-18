import bart
import weather
import logging
import os
import time

if os.uname().sysname == 'Linux':
    import scrollphat
elif os.uname().sysname == 'Darwin':
    import fake_scrollphat as scrollphat


def scroll_cycle(output):
    scrollphat.update()
    scrollphat.write_string(output)
    time.sleep(2)
    scrollphat.clear()


if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    scrollphat.set_brightness(4)
    current_weather = weather.get_weather()

    while(True):
        try:
            next_bart = bart.get_bart()
            scroll_cycle("its")
            scroll_cycle("{feelslike}".format(**current_weather))
            scroll_cycle("Bart")
            scroll_cycle("{}".format(next_bart))
            time.sleep(5)
        except KeyboardInterrupt:
            scrollphat.clear()
            quit()
