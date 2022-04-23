import json
import time
import datetime
import sys
from   requests import get

import base64
import os

#openweathermap.org API Key:
apiKey    = 'ce6df52db591b8e6b40f75c864518b61'
#Minneapolis, MN, USA.
lattitude = '44.9398'
longitude = '-93.2533'
units     = 'imperial'

url = 'http://api.openweathermap.org/data/2.5/onecall?lat=' + lattitude + '&lon=' + longitude + '&exclude=minutely,hourly&appid=' + apiKey + '&units=' + units
while True:

    try:
        weatherData = get(url).json()
        with open('/var/www/html/mount/data/weatherData.json', 'w') as f:
	        json.dump(weatherData, f, indent = 2)
        time.sleep(600000)

    except:
        pass
