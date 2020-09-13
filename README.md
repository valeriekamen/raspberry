Library: https://github.com/pimoroni/scroll-phat/blob/master/library/scrollphat/__init__.py

To run script:
1. ssh -A pi@raspberrypi.local
2. cd raspberry
3. python3 __.py
    a. nohup python3 __.py
      1. to print output to file, and skip errors

To develop:
1. Work on file from src/raspberry local
2. Print to terminal instead of pi
3. Change to pi output before scp
4. cd raspberry
5. scp __.py pi@raspberrypi.local:raspberry

Set up on wifi: 
1. Follow https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
    a. Create config file and drag into the boot


Scripts:
Display.py
Scrolls weather for Oakland, CA and BART arrival times for MacArthur Station
Display2.py
Scrolls weather and US AQI for San Francisco
