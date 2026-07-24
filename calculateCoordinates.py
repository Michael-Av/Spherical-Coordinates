import numpy as np
import sys
import math
import datetime
import siderealTime as st
import readLeData as rld

PI = np.pi

# +x = north
# +y = west
# +z = up (towards zenith)

# # Observer coordinates
# latitude=-35.3
# longitude=149.1310

# datetime.datetime(YEAR, MON, DAY, HOUR, MIN, SEC)
time = datetime.datetime(2026, 7, 25, 0, 0, 0)

# # Object coordinates
# azimuth=283.7
# altitude=71.5

def calcCoords(altitude, azimuth, latitude, longitude):
	siderealTime = st.getSiderealTime(latitude, longitude, time)

	zenithVec = np.array([0, 0, 1])
	poleVec = np.array([1, 0, np.tan(latitude)]) # Could be negative or positive
	objectVec = np.array([np.cos(azimuth), -1 * np.sin(azimuth), np.tan(altitude)])

	# normalize vectors
	zenithVec = zenithVec / np.linalg.norm(zenithVec)
	poleVec = poleVec / np.linalg.norm(poleVec)
	objectVec = objectVec / np.linalg.norm(objectVec)

	print("zenithVec: ", zenithVec) 
	print("poleVec: ", poleVec)
	print("objectVec: ", objectVec)
	print("poleVec.dot(objectVec): ", poleVec.dot(objectVec))
	dotProduct = math.trunc(poleVec.dot(objectVec)*1000) / 1000.0

	#print("zenith: ", zenithVec)
	#print("pole: ", poleVec)
	#print("object: ", objectVec)

	# sides of astronomical triangle
	OP = np.arccos(dotProduct) # 0-PI
	PZ = PI / 2 - latitude # 0-PI
	ZO = PI / 2 - altitude # 0-PI/2

	print("OP: ", OP)
	print("PZ: ", PZ)
	print("ZO: ", ZO)

	# le mathematique
	declination = PI / 2 - OP # -PI/2 -> PI/2
	toArccos = (np.cos(ZO) - np.cos(OP) * np.cos(PZ)) / (np.sin(OP) * np.sin(PZ))
	print(toArccos)
	if (toArccos > 1):
		toArccos = 1
	if (toArccos < -1):
		toArccos = -1
	hourAngle = np.arccos(toArccos)
	if (azimuth < PI):
		hourAngle = 2 * PI - hourAngle
	rightAscension = siderealTime - hourAngle
	if rightAscension < 0:
		rightAscension += 2 * PI

	print("declination = ", declination*180/PI)
	print("Sidereal time: ", siderealTime*12/PI)
	print("hourAngle: ", hourAngle*12/PI)
	print("rightAscension = ", rightAscension*12/PI)
	print("ANSWER!!!!", rld.findNearestStar(rightAscension, declination))

def calcAzimuthalCoords(starName, latitude, longitude):
	RA, dec = rld.getEquatorialCoords(starName)
	siderealTime = st.getSiderealTime(latitude, longitude, time)

	# le Plan

	# azimuth = 360° - <PZO
	# altitude = 90° - <ZO

	# knowns:
	# <ZPO (from HA <-- RA, ST) √
	# <PZ (90° - lat) √
	# <OP (90° - dec) √

	# knowns --> <ZO --> alt (90° - ZO) √
	# PZ, ZO, PO --> <PZO (law of cosines) --> azm (360° - <PZO) √

	HA = siderealTime - RA
	if HA < 0:
		HA += 2*PI
	ZPO = HA
	print("HA:",HA)
	if ZPO>PI:
		ZPO=2*PI-ZPO
	PZ = PI/2 - latitude
	OP = PI/2 - dec

	cosOZ = np.cos(OP)*np.cos(PZ) + np.sin(OP)*np.sin(PZ)*np.cos(ZPO)
	OZ = np.arccos(cosOZ)
	altitude = PI/2 - OZ

	# print("ZPO:",ZPO)
	# sinPZO = np.sin(OP)*np.sin(ZPO)/np.sin(OZ)
	# print("SinPZO",sinPZO)
	# PZO = np.arcsin(sinPZO)
	# if HA>PI:
	# 	PZO+=PI
	# print("PZO:",PZO*180/PI)
	# azimuth = 2*PI - PZO

	cosPZO = (np.cos(OP)-np.cos(PZ)*np.cos(OZ))/(np.sin(PZ)*np.sin(OZ))
	print("CosPZO:",cosPZO)
	PZO = np.arccos(cosPZO)
	if (HA > PI):
		PZO=2*PI-PZO
	print("PZO:",PZO*180/PI)
	azimuth = 2*PI - PZO


	if(azimuth>2*PI):
		azimuth=azimuth-2*PI

	print("Altitude:", altitude*180/PI, "\nAzimuth:", azimuth*180/PI)

lat = -26.20500
long = 28.04972
# calcAzimuthalCoords("Pollux", lat*PI/180, long*PI/180)
alt=-82
azi=44
calcCoords(alt*PI/180, azi*PI/180, lat*PI/180, long*PI/180)

# commandLength = len(sys.argv)

# altitude = float(sys.argv[1])*PI/180
# azimuth = float(sys.argv[2])*PI/180
# # python3 calculateCoordinates.py altitude azimuth latitude longitude
# if commandLength == 5:
# 	lat = float(sys.argv[3])*PI/180
# 	long = float(sys.argv[4])*PI/180
# 	calcCoords(altitude, azimuth, lat, long)
# # python3 calculateCoordinates.py altitude azimuthHour azimuthMinute latitude longitude
# elif commandLength == 6:
# 	azimuthHr = float(sys.argv[2]) * PI / 12
# 	azimuthMin = float(sys.argv[3]) * PI / 720
# 	lat = float(sys.argv[4])*PI/180
# 	long = float(sys.argv[5])*PI/180
# 	calcCoords(altitude, azimuthHr + azimuthMin, lat, long)
# # python3 calculateCoordinates.py altitude azimuth city
# elif commandLength == 4:
# 	lat = 0
# 	long = 0
# 	city = sys.argv[3]
# 	if city.lower().strip() == "binghamton":
# 		lat = 42.0894
# 		long = -75.9695
# 	elif city.lower().strip() == "rochester":
# 		lat = 43.1306
# 		long = -77.6260
# 	elif city.lower().strip() == "new york city" or city.lower().strip() == "nyc":
# 		lat = 40.7128
# 		long = -74.0060
# 	elif city.lower().strip() == "Johannesburg":
# 		lat = -26.20500
# 		long = 28.04972
# 	else:
# 		print("City not recognized")
# 		exit()
# 	lat = lat * PI / 180
# 	long = long * PI / 180
# 	calcCoords(altitude, azimuth, lat, long)
# else:
# 	print("Command not recognized: try using a correct format L")
# 	exit()
