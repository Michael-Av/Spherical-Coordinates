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
time = datetime.datetime(2026, 1, 15, 20, 0, 0)

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

calcCoords(float(sys.argv[1])*PI/180, float(sys.argv[2])*PI/180, float(sys.argv[3])*PI/180, float(sys.argv[4])*PI/180)
