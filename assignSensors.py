# steve.a.mccluskey@gmail.com
# Utility that shows all OneWire temp sensors on the bus and allows you to assign them to the rooms and writes the configuration to the sensorIndex.config file.




import os
import time
import glob
import json
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensorIds = os.listdir("/sys/bus/w1/devices")
config_file = "/home/pi/weatherStation/sensorIndex.config"

rooms     = ['livingRoom', 'upstairs', 'office', 'guestRoom', 'stevesRoom', 'attic', 'basement', 'freezer', 'sammyDoor', 'garage', 'outside', 'incubator', 'fruiting']
roomNames = ["Living Room  ", "Upstairs     ", "Office       ", "Guest Room   ", "Steve's Room ", "Attic        ", "Basement     ", "Freezer      ", "Sammy's Door ", "Garage       ", "Outside      ", "Incubator    ", "Fruit Chamber"]

ids = [0] * len(rooms)

#open config file and get assignments:
def get_assignments():


	f = open(config_file, 'r')
	lines = f.readlines()
	f.close()
#
	count = len(lines)
	print("ASSIGNMENTS BY ROOM:")
	#length of config file:
	for i in range(count):
		#length of range rooms
		for x in range(len(rooms)):
			#look for each room in each line of config file:
			if (lines[i].find(str(rooms[x])) != -1):
				slot = lines[i].find('=')
				ids[i] = str(lines[i][slot + 2 : slot + 17])

				if (ids[i].find('null') != -1):
					print(str(roomNames[x]) + ": unassigned.")
				else:
					print(str(roomNames[x]) + ": assigned to : " + str(ids[i]))


	#end for
	print(" ")
#end def




def read_temp(file):
	device_file = "/sys/bus/w1/devices/" + file + "/w1_slave"
	f = open (device_file, 'r')
	lines = f.readlines()
	f.close()

	equals_pos = lines[1].find('t=')

	if (equals_pos != -1):
		temp_string = lines[1][equals_pos + 2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = format(float(temp_c * 9.0 / 5.0 + 32.0), '.1f')
		return temp_f
	#end if
#end def


def reassign_sensor_to_room():
	assignments = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
	assigned    = [False,  False,  False,  False,  False,  False,  False,  False,  False,  False,   False,  False,  False,  False]
	print("")
	for sensor in range (len(sensorIds)):
		if (sensorIds[sensor].find('28-') != -1):
		#skip w1_bus_master1 folder

			print("Assign " + str(sensorIds[sensor]) + " to:")
			if (assigned[0] == False):
				print("1: Living Room")

			if (assigned[1] == False):
				print("2: Upstairs")

			if (assigned[2] == False):
				print("3: Office")

			if (assigned[3] == False):
				print("4: Guest Room")

			if (assigned[4] == False):
				print("5: Steve's Room")

			if (assigned[5] == False):
				print("6: Attic")

			if (assigned[6] == False):
				print("7: Basement")

			if (assigned[7] == False):
				print("8: Freezer")

			if (assigned[8] == False):
				print("9: Sammy's Door")

			if (assigned[9] == False):
				print("10: Garage")

			if (assigned[10] == False):
				print("11: Outside")

			if (assigned[11] == False):
				print("12: Incubator")

			if (assigned[12] == False):
				print("13: Fruiting Chamber")
				print(" ")

			print("Input 1 - " + str(len(rooms)) + ". Enter zero to leave unassigned.")
			assignment = int(input())

			while (assignment > len(rooms)):
				print("Assignment out of range. Please enter 0 - " + str(len(rooms)) + ".")
				assignment = int(input())

			if (assignment == 0):
				print("Sensor " + str(sensorIds[sensor]) + " remains unassigned.")
				print("")

			for x in range(1, len(sensorIds)):
				if (assignment == x) :
					print("Sensor " + str(sensorIds[sensor]) +  " assigned to " + str(roomNames[x - 1]))
					assignments[x - 1] = str(sensorIds[sensor])
					assigned[x - 1] = True
					print("")



		#end if
	#end for sensor
	print(" ")

	f = open(config_file, 'w')
	f.write("livingRoom = " + str(assignments[0])  + "\n")
	f.write("upstairs   = " + str(assignments[1])  + "\n")
	f.write("office     = " + str(assignments[2])  + "\n")
	f.write("guestRoom  = " + str(assignments[3])  + "\n")
	f.write("stevesRoom = " + str(assignments[4])  + "\n")
	f.write("attic      = " + str(assignments[5])  + "\n")
	f.write("basement   = " + str(assignments[6])  + "\n")
	f.write("freezer    = " + str(assignments[7])  + "\n")
	f.write("sammyDoor  = " + str(assignments[8])  + "\n")
	f.write("garage     = " + str(assignments[9])  + "\n")
	f.write("outside    = " + str(assignments[10]) + "\n")
	f.write("incubator  = " + str(assignments[11]) + "\n")
	f.write("fruiting   = " + str(assignments[12]) + "\n")
	f.close()
#	return
#end def

def show_assignments_by_sensor():
	print("ASSIGNMENTS BY SENSOR:")
	for sensor in range(len(sensorIds)):
		sensorFound = False
		if(sensorIds[sensor].find('28-') != -1):

			for x in range(len(ids)):
				if (str(ids[x]) == str(sensorIds[sensor])):
					print("Sensor ID: " + str(sensorIds[sensor])+ " assigned to : " + str(roomNames[x]))
					sensorFound = True
					break


			if (sensorFound == False):
				print("Sensor ID: " + str(sensorIds[sensor]) + " unassigned.")

	print("")

#end def show_assignments_by_sensor()




#start
print(" ")
get_assignments()
show_assignments_by_sensor()

print("FOUND " + str((len(sensorIds) -1)) + " DEVICES ON BUS:")
for sensor in range(len(sensorIds)):
	if (sensorIds[sensor].find('28-') != -1):
		temp = read_temp(sensorIds[sensor])
		print("Sensor ID: " + str(sensorIds[sensor]) + ". Temp = " + str(temp) + "F.")


print(" ")
print(" ")
print("Do you want to reassign sensors? Y/N?")
sensorReassign = input()
#print(str(sensorReassign))

if (sensorReassign == 'y' or sensorReassign == 'Y'):
	print("Do you want to")
	print("1, Reassign all sensors to rooms?")
	#print("2, Assign only unassigned sensors?")
	sensorReassignType = int(input())

	if (sensorReassignType == 1):
		reassign_sensor_to_room()

	if (sensorReassignType == 2):
		print("")
		#assign_unnasigned_sensor_to_room()


print("Done.")

#end all


