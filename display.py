import bart
import weather
import logging
import os
import time

if os.uname().sysname == 'Linux':
    import scrollphat
elif os.uname().sysname == 'Darwin':
    import fake_scrollphat as scrollphat


def flash_cycle(output):
    # no scroll, just prints one message at a time
    scrollphat.update()
    scrollphat.write_string(output)
    time.sleep(2)
    scrollphat.clear()


# def scroll_message(output):
#     scrollphat.write_string(output)
#     scrollphat.update()

#     while(True):
#         try:
#             scrollphat.scroll()
#             scrollphat.update()
#             time.sleep(0.2)
#         except KeyboardInterrupt:
#             return

def scroll_message_once():
    length = scrollphat.buffer_len()

    for i in range(length):
        try:
            scrollphat.scroll()
            time.sleep(0.1)
        except KeyboardInterrupt:
            scrollphat.clear()
            break


def update_next_bart():
    next_barts_list = bart.get_bart()
    next_barts_str = ', '.join(next_barts_list)
    return next_barts_str


if(__name__ == '__main__'):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    scrollphat.set_brightness(4)
    current_weather = weather.get_weather()
    feelslike = "{}".format(current_weather.get('feelslike'))

    while True:
        try:
            next_barts_str = update_next_bart()
            msg = "Its {}. Bart in {}".format(feelslike, next_barts_str)
            scrollphat.write_string(msg)
            scroll_message_once()
        except KeyboardInterrupt:
            scrollphat.clear()
            break
