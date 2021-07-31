# WeatherStation
Raspberry Pi Weather Station
steve.a.mccluskey@gmail.com

As of July, 2021, I've spent a little over a year off and on developing this weather station. It hangs on the wall in my living room. It was my first python project. I used nano in the console to edit everything and have recently started doing all the web development in VS Code and its a night and day difference. I'll never go back. Originally I was hesitant to do any development in an IDE because to test the code, I have to FTP it back to the Pi and run it remotely, but the time saved by using VS Code more than makes up for it. The whole project was a very ambitious one as I had almost no experience programming in python. I've worked with Arduino and C++ for several years now and this was completely different. I am self-taught and have no formal education in computer science. I have an associates degree in Manufacturing Technology.

As of the time of this writing, I don't know how to make any install scripts so if you download and run this, there may be some editing required and/or making sure directories are in the right place. Comments and suggestions are always welcome. 

Some things I learned along the way:
1) SD cards get corrupted quickly. Installing a USB stick and writing the temp sensor data and weather data to it instead of the main SD card solved most of this. The same data being over written in the same place every few seconds has little to no effect on USB sticks. Even if it does, replacing it is quick and easy and doesn't require you to reinstall Raspbian and start from scratch every few months.
2) Take lots of notes. Every thing you install, such as software dependencies and misc commands in the console will be needed again eventually and it can be quite frustrating to remember what I did a week later to get one piece of code to work. 
3) More added as I think of it.
