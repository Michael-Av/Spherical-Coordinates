import numpy as np
import sys
import math

PI = np.pi

# +x = north
# +y = west
# +z = up (towards zenith)

# Observer coordinates
latitude=89
siderealTime=0

# Object coordinates
azimuth=0
altitude=89

def calcCoords(azimuth, altitude, latitude, siderealTime):
	# define vectors
	zenithVec = np.array([0, 0, 1])
	poleVec = np.array([1, 0, np.tan(latitude)])
	objectVec = np.array([np.cos(azimuth), -1 * np.sin(azimuth), np.tan(altitude)])

	# normalize vectors
	zenithVec = zenithVec / np.linalg.norm(zenithVec)
	poleVec = poleVec / np.linalg.norm(poleVec)
	objectVec = objectVec / np.linalg.norm(objectVec)

	#print(poleVec)
	#print(objectVec)
	#print(poleVec.dot(objectVec))
	dotProduct = math.trunc(poleVec.dot(objectVec)*1000) / 1000.0
	#print(dotProduct)
	#print("zenith: ", zenithVec)
	#print("pole: ", poleVec)
	#print("object: ", objectVec)

	# sides of astronomical triangle
	OP = np.arccos(dotProduct)
	PZ = PI / 2 - latitude
	ZO = PI / 2 - altitude

	# le mathimatique
	declination = PI / 2 - OP
	hourAngle = np.arccos((np.cos(ZO) - np.cos(OP) * np.cos(PZ)) / (np.sin(OP) * np.sin(PZ)))
	rightAscension = siderealTime - hourAngle

	print("declination = ", declination)
	print("rightAscension = ", rightAscension)

calcCoords(azimuth, altitude, latitude, siderealTime)

