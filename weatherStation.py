# -------------------------------
# WeatherStation for Raspberry Pi 3 Model B+
# steve.a.mccluskey@gmail.com
#
# Code adapted from youtube.com/watch?v=MWKAitSX3vg
# Channel educ8s.tv
# Video name "Raspberry Pi Project: Touch Weather Station using a DHT22 and a Raspberry Pi 3 with TKInter GUI
#
# This program uses readings from several Dallas DS18B20 temp sensors and displays on the LCD along with on a website.
# Temps are collected from a background process called updateSensors.py and written to a JSON file called sensorValues.JSON
# which is located in the web folder at /var/www/html/mount/data. This program reads the JSON file. The webpage also reads it so there's
# minimal interferance between programs.
# Sensors are zero indexed.  The sensors are assigned to their respective labels by their index number.
# Use readSensors.py to print their index number, digital ID and current temp to the console.
# Edit sensorIndex.config to assign their correct indexes to this screen. Config file is read before reading json file and will update
# sensors without the need to relaunch this app.

#
# Hardware Used:
# Raspberry Pi 3 Model B+
# Raspberry Pi Official 7" Touch Screen
# Adafruit Perma-Proto HAT for Pi Mini Kit - No EEPROM, adafruit.com/product/2310
# Sparkfun RJ45 Breakout sparkfun.com/products/716
# Sparkfun RJ45 8-Pin Connector sparkfun.com/products/643
# Dallas OneWire DS18B20 Digital Temp Sensors
#
#
#
#
# ------------
# GPIO Pins used:
# Pys Name      BCM        Patched Thru          Patched To
# 1 ) 3.3v		-> cat5e orange       -> 3.3v
# 2 ) 5.0v
# 3 ) SDA       GPIO 2  -> cat5e white/brown  -> I2C SDA
# 4 ) 5.0v
# 5 ) SCL	GPIO 3	-> cat5e brown        -> I2C SCL
# 6 ) Gnd		-> cat5e white/orange -> Gnd
# 7 ) GPIO 7 -> GPIO 4  -> cat5e white/green  -> OneWire Bus
# 8 ) TXD	GPIO 14
# 9 ) Gnd
# 10) RXD	GPIO 15
# 11) GPIO 0 -> GPIO 17
# 12) GPIO 1 -> GPIO 18
# 13) GPIO 2 -> GPIO 27 -> cat5e blue         -> Main Door Sensor
# 14) Gnd
# 15) GPIO 3 -> GPIO 22 -> cat5e white/blue   -> Side Door Sensor
# 16) GPIO 4 -> GPIO 23 -> cat5e green        -> Side Door Lock Sensor
# 17) 3.3v
# 18) GPIO 5    GPIO 24
# 19) SPI MOSI  GPIO 10
# 20) Gnd
#
# Pys Name      BCM        Patched Thru         Patched To
# 21) SPI MISO  GPIO 9
# 22) GPIO 6    GPIO 25
# 23) SPI SCLK  GPIO 11
# 24) SPI CE0   GPIO 8
# 25) Gnd
# 26) SPI CE1   GPIO 7
# 27) ID SD
# 28) ID SC
# 29) 		GPIO 5
# 30) Gnd
# 31) 		GPIO 6
# 32)		GPIO 12
# 33)		GPIO 13
# 34) Gnd
# 35) PCM	GPIO 19
# 36) 		GPIO 16
# 37)		GPIO 26
# 38)		GPIO 20
# 39) Gnd
# 40) 		GPIO 21

# -------
# Cat5e Pinout :
# White/Orange : Gnd
# Orange       : 3.3v
# White/Green  : OneWire
# Blue         : Main Door Sensor
# White/Blue   : Side Door Sensor
# Green        : Side Door Lock Sensor
# White/Brown  : I2C SDA
# Brown        : I2C SCL


from   Tkinter import *
import Tkinter as tk
from   Tkinter import Canvas
from   PIL import ImageTk, Image
import threading
import tkFont
import RPi.GPIO as GPIO
import json
import time
import datetime
import sys
from   requests import get
from   urllib2 import urlopen
import base64
import os

os.system("sudo python /home/pi/weatherStation/getTemps.py &")



#openweathermap.org API Key:
apiKey    = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#Minneapolis, MN, USA.
lattitude = '44.9398'
longitude = '-93.2533'
units     = 'imperial'


#digital door sensor pins:
mainDoorPin     = 27
sideDoorPin     = 22
sideDoorLockPin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(mainDoorPin,     GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sideDoorPin,     GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sideDoorLockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global garageOpenIcon
global garageClosedIcon
global doorUnlockedIcon
global doorLockedIcon
global doorOpenIcon

global mainDoorLabel
global sideDoorLabel
global weatherIconLabel

degree_sign = u"\N{DEGREE SIGN}"

root = tk.Tk()

backgroundImage  = PhotoImage(file = "/home/pi/weatherStation/img/background.png")
garageOpenIcon   = PhotoImage(file = "/home/pi/weatherStation/img/garageOpen.png")
garageClosedIcon = PhotoImage(file = "/home/pi/weatherStation/img/garageClosed.png")
doorLockedIcon   = PhotoImage(file = "/home/pi/weatherStation/img/doorLocked.png")
doorUnlockedIcon = PhotoImage(file = "/home/pi/weatherStation/img/doorUnlocked.png")
doorOpenIcon     = PhotoImage(file = "/home/pi/weatherStation/img/doorOpen.png")

#image labels:
background = Label(image = backgroundImage)
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

mainDoorLabel = Label(root, borderwidth = 0)
sideDoorLabel = Label(root, borderwidth = 0)

mainDoorLabel.place(x = 150, y = 100)
sideDoorLabel.place(x = 260, y = 100)

weatherIconLabel = Label(root)
weatherIconLabel.place (x = 30, y = 60)

#temp sensor strings:
insideAvgTemp  = StringVar()
tempLivingRoom = StringVar()
tempUpstairs   = StringVar()
tempBasement   = StringVar()
tempOut        = StringVar()
tempGarage     = StringVar()
tempFreezer    = StringVar()
currentTime    = StringVar()
timeStamp      = StringVar()
tempHigh       = StringVar()
tempLow        = StringVar()
tempFeelsLike  = StringVar()
humidity       = StringVar()
dailyCondition = StringVar()

#temp sensor labels:
insideAvgTempLabel = Label(root, fg = "blue", background = "#00dbde", text = "In: ", font = ("Helvetica", 30), borderwidth = 0)
insideAvgTempLabel.place(x = 20, y = 210)

insideAvgTempValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = insideAvgTemp, font = ("Helvetica", 68, "bold"), borderwidth = 0)
insideAvgTempValueLabel.place(x = 100, y = 180)

tempOutLargeLabel = Label(root, fg = "blue", background = "#00dbde", text = "Out: ", font = ("Helvetica", 30), borderwidth = 0)
tempOutLargeLabel.place(x = 20, y = 320)

tempOutLargeValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = tempOut, font = ("Helvetica", 68, "bold"), borderwidth = 0)
tempOutLargeValueLabel.place(x = 100, y = 280)

tempFeelsLikeLabel = Label(root, fg = "blue", background = "#00dbde", text = "Feels Like:", font = ("Helvetica", 30), borderwidth = 0)
tempFeelsLikeLabel.place(x = 20, y = 420)

tempFeelsLikeValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = tempFeelsLike, font = ("Helvetica", 48, "bold"), borderwidth = 0)
tempFeelsLikeValueLabel.place(x = 230, y = 400)

currentTimeLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = currentTime, font = ("Helvetica", 40), borderwidth = 0)
currentTimeLabel.place(x = 190, y = 15)

todayLabel = Label(root, fg = "blue", background = "#00dbde", text = "Today:", font = ("Helvetica", 30), borderwidth = 0)
todayLabel.place(x = 440, y = 90)

todayLabelValue = Label(root, fg = "blue", background = "#00dbde", textvariable = dailyCondition, font = ("Helvetica", 30, "bold"))
todayLabelValue.place(x = 590, y = 90)

tempHighLabel = Label(root, fg = "blue", background = "#00dbde", text = "High:", font = ("Helvetica", 25), borderwidth = 0)
tempHighLabel.place(x = 440, y = 140)

tempHighLabelValue = Label(root, fg = "blue", background = "#00dbde", textvariable = tempHigh, font = ("Helvetica", 25, "bold"), borderwidth = 0)
tempHighLabelValue.place(x = 520, y = 140)

tempLowLabel = Label(root, fg = "blue", background = "#00dbde", text = "Low:", font = ("Helvetica", 25), borderwidth = 0)
tempLowLabel.place(x = 600, y = 140)

tempLowLabelValue = Label(root, fg = "blue", background = "#00dbde", textvariable = tempLow, font = ("Helvetica", 25, "bold"), borderwidth = 0)
tempLowLabelValue.place(x = 685, y = 140)

humidityLabel = Label(root, fg = "blue", background = "#00dbde", text = "Humidity:", font = ("Helvetica", 25), borderwidth = 0)
humidityLabel.place(x = 440, y = 190)

humidityLabelValue = Label(root, fg = "blue", background = "#00dbde", textvariable = humidity, font = ("Helvetica", 25, "bold"), borderwidth = 0)
humidityLabelValue.place(x = 685, y = 190)

tempLivingRoomLabel = Label(root, fg = "blue", background = "#00dbde", text = "Living Room: ", font = ("Helvetica", 25), borderwidth = 0)
tempLivingRoomLabel.place(x = 440, y = 230)

tempLivingRoomValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = tempLivingRoom, font = ("Helvetica", 25, "bold"), borderwidth = 0)
tempLivingRoomValueLabel.place(x = 685, y = 230)

tempUpstairsLabel = Label(root, fg= "blue", background = "#00dbde", text = "Upstairs: ", font = ("Helvetica", 25), borderwidth = 0)
tempUpstairsLabel.place(x = 440, y = 270)

tempUpstairsValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = tempUpstairs, font = ("Helvetica", 25, "bold"), borderwidth = 0)
tempUpstairsValueLabel.place(x = 685, y = 270)

tempBasementLabel = Label(root, fg = "blue", background = "#00dbde", text = "Basement: ", font = ("Helvetica", 25), borderwidth = 0)
tempBasementLabel.place(x = 440, y = 350)

tempBasmentValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = tempBasement, font = ("Helvetica", 25, "bold"), borderwidth = 0)
tempBasmentValueLabel.place(x = 685, y = 350)

tempGarageLabel = Label(root, fg = "blue", background = "#00dbde", text = "Garage: ", font = ("Helvetica", 25), borderwidth = 0)
tempGarageLabel.place(x = 440, y = 310)

tempGarageValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = tempGarage, font = ("Helvetica", 25, "bold"), borderwidth = 0)
tempGarageValueLabel.place(x = 685, y = 310)

tempFreezerLabel = Label(root, fg = "blue", background = "#00dbde", text = "Freezer: ", font = ("Helvetica", 20), borderwidth = 0)
tempFreezerLabel.place(x = 440, y = 395)

tempFreezerValueLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = tempFreezer, font = ("Helvetica", 25, "bold"), borderwidth = 0)
tempFreezerValueLabel.place(x = 685, y = 390)

timeStampLabel = Label(root, fg = "blue", background = "#00dbde", textvariable = timeStamp, font = ("Helvetica", 20), borderwidth = 0)
timeStampLabel.place(x = 440, y = 440)

root.attributes("-fullscreen", True)
root.config(cursor = "none")

exitButton = tk.Button(root, fg = "white", text = "X", font = ("Helvetica", 20, "bold"), command = exit, bg = "red")
exitButton.place(x = 760, y = 0)


def exit():
	root.quit()


def updateTemps():
	dateTime_value = []

	try:



		with open('/var/www/html/mount/data/sensorValuesNew.json', 'r') as f:
			data       = f.read()
			dataString = json.loads(data)
		f.close()

		for dateTime in dataString['timestamp']:
			dateTime_value = (dateTime['dateTime'])



		tempLivingRoom.set(str(dataString['sensors']['livingRoom']['temp']) + degree_sign + "F")
		tempOut       .set(str(dataString['sensors']['outside']['temp'])    + degree_sign + "F")
		tempGarage    .set(str(dataString['sensors']['garage']['temp'])     + degree_sign + "F")
		tempUpstairs  .set(str(dataString['sensors']['upstairs']['temp'])   + degree_sign + "F")
		tempBasement  .set(str(dataString['sensors']['basement']['temp'])   + degree_sign + "F")
		tempFreezer   .set(str(dataString['sensors']['freezer']['temp'])    + degree_sign + "F")

		timeStamp     .set(str(dateTime_value))

		avg = format( float( float( int(dataString['sensors']['livingRoom']['temp']) ) + float( int(dataString['sensors']['upstairs']['temp']) ) / 2.0), '.1f')
		insideAvgTemp.set(str(avg) + degree_sign + "F")

	except:
		pass

	root.after(2000, updateTemps)


def getDoors():
	#side door open and unlocked:
	if(GPIO.input(sideDoorPin) == GPIO.HIGH):
		sideDoorLabel.configure(image = doorOpenIcon)
		sideDoorLabel.image = doorOpenIcon

	#closed and unlocked:
	elif(GPIO.input(sideDoorPin) == GPIO.LOW):
		if(GPIO.input(sideDoorLockPin) == GPIO.HIGH):
			sideDoorLabel.configure(image = doorUnlockedIcon)
			sideDoorLabel.image = doorUnlockedIcon

		elif(GPIO.input(sideDoorPin) == GPIO.LOW):
			sideDoorLabel.configure(image = doorLockedIcon)
			sideDoorLabel.image = doorLockedIcon

	#main door:
	if(GPIO.input(mainDoorPin) == GPIO.HIGH):
		mainDoorLabel.configure(image = garageOpenIcon)
		mainDoorLabel.image = garageOpenIcon

	else:
		mainDoorLabel.configure(image = garageClosedIcon)
		mainDoorLabel.image = garageClosedIcon

	root.after(2000, getDoors)


def getTime():
	currentTime.set(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
	root.after(500, getTime)

def getWeather():
	#get data from openweathermap.org:
	url = 'http://api.openweathermap.org/data/2.5/onecall?lat=' + lattitude + '&lon=' + longitude + '&exclude=minutely,hourly&appid=' + apiKey + '&units=' + units

	try:
		weatherData = get(url).json()

#		print weatherData

		#set values from json data:
		humidity.set(str(weatherData['current']['humidity']) + "%")
		tempFeelsLike.set(str(int(round(weatherData['current']['feels_like']))) + degree_sign + "F")
		tempHigh.set(str(int(round(weatherData['daily'][0]['temp']['max']))) + degree_sign + "F")
		tempLow.set(str(int(round(weatherData['daily'][0]['temp']['min']))) + degree_sign + "F")
		dailyCondition.set(str(weatherData['daily'][0]['weather'][0]['main']))
		weatherIconCode = weatherData['current']['weather'][0]['icon']

		#get weather icon and convert:
		imageUrl = "http://openweathermap.org/img/wn/" + weatherIconCode + "@2x.png"
		weatherIconByt = urlopen(imageUrl).read()
		weatherIconB64 = base64.encodestring(weatherIconByt)

		weatherIcon = PhotoImage(data = weatherIconB64)
		weatherIconLabel.configure(image = weatherIcon)
		weatherIconLabel.image = weatherIcon

		#weatherData["current"].append({'timeStamp': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))})

		with open('/var/www/html/mount/data/weatherData.json', 'w') as f:
			json.dump(weatherData, f, indent = 2)
	except:
		pass

	#update every 10 minutes
	root.after(600000, getWeather)


root.after(1000, getWeather)
root.after(1000, getTime)
root.after(1001, updateTemps)
root.after(1000, getDoors)
root.mainloop()
