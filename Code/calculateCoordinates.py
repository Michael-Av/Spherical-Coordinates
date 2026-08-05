import numpy as np
import math
import Code.siderealTime as st
import Code.readLeData as rld

PI = np.pi

def calcCelestialCoords(altitude, azimuth, latitude, longitude, time):
	minLatitude=-PI/2.01
	maxLatitude=PI/2.01
	latitude = min(maxLatitude, max(minLatitude, latitude))
	siderealTime = st.getSiderealTime(latitude, longitude, time)

	zenithVec = np.array([0, 0, 1])
	poleVec = np.array([1, 0, np.tan(latitude)]) # Could be negative or positive
	objectVec = np.array([np.cos(azimuth), -1 * np.sin(azimuth), np.tan(altitude)])

	# normalize vectors
	zenithVec = zenithVec / np.linalg.norm(zenithVec)
	poleVec = poleVec / np.linalg.norm(poleVec)
	objectVec = objectVec / np.linalg.norm(objectVec)

	# print("zenithVec: ", zenithVec) 
	# print("poleVec: ", poleVec)
	# print("objectVec: ", objectVec)
	# print("poleVec.dot(objectVec): ", poleVec.dot(objectVec))
	dotProduct = math.trunc(poleVec.dot(objectVec)*1000) / 1000.0

	#print("zenith: ", zenithVec)
	#print("pole: ", poleVec)
	#print("object: ", objectVec)

	# sides of astronomical triangle
	OP = np.arccos(dotProduct) # 0-PI
	PZ = PI / 2 - latitude # 0-PI
	ZO = PI / 2 - altitude # 0-PI/2

	# print("OP: ", OP)
	# print("PZ: ", PZ)
	# print("ZO: ", ZO)

	# le mathematique
	declination = PI / 2 - OP # -PI/2 -> PI/2
	toArccos = (np.cos(ZO) - np.cos(OP) * np.cos(PZ)) / (np.sin(OP) * np.sin(PZ))
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
	return [rightAscension, declination]

def calcHorizontalCoords(rightAscension, declination, latitude, longitude, siderealTime):
	minLatitude=-PI/2.01
	maxLatitude=PI/2.01
	latitude = min(maxLatitude, max(minLatitude, latitude))
	#print(latitude)

	# le Plan

	# azimuth = 360° - <PZO
	# altitude = 90° - <ZO

	# knowns:
	# <ZPO (from HA <-- RA, ST) √
	# <PZ (90° - lat) √
	# <OP (90° - dec) √

	# knowns --> <ZO --> alt (90° - ZO) √
	# PZ, ZO, PO --> <PZO (law of cosines) --> azm (360° - <PZO) √

	HA = siderealTime - rightAscension
	if HA < 0:
		HA += 2*PI
	ZPO = HA
	# print("HA:",HA)
	if ZPO>PI:
		ZPO=2*PI-ZPO
	PZ = PI/2 - latitude
	OP = PI/2 - declination

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
	# print("CosPZO:",cosPZO)
	PZO = np.arccos(cosPZO)
	if (HA > PI):
		PZO=2*PI-PZO
	# print("PZO:",PZO*180/PI)
	azimuth = 2*PI - PZO


	if(azimuth>2*PI):
		azimuth=azimuth-2*PI

	# print("Altitude:", altitude*180/PI, "\nAzimuth:", azimuth*180/PI)
	return [altitude, azimuth]