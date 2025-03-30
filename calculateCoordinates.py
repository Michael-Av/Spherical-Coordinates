import numpy as np

PI = np.pi

# +x = north
# +y = west
# +z = up (towards zenith)

# horizontal coordinates
azimuth = PI / 3
altitude = PI / 4

# observer details
latitude = PI / 6
siderealTime = PI

# define vectors
zenithVec = np.array([0, 0, 1])
poleVec = np.array([1, 0, np.tan(latitude)])
objectVec = np.array([np.cos(azimuth), -1 * np.sin(azimuth), np.tan(altitude)])

# normalize vectors
zenithVec = zenithVec / np.linalg.norm(zenithVec)
poleVec = poleVec / np.linalg.norm(poleVec)
objectVec = objectVec / np.linalg.norm(objectVec)

#print("zenith: ", zenithVec)
#print("pole: ", poleVec)
#print("object: ", objectVec)

# sides of astronomical triangle
OP = np.arccos(poleVec.dot(objectVec))
PZ = PI / 2 - latitude
ZO = PI / 2 - altitude

# le mathimatique
declination = PI / 2 - OP
hourAngle = np.arccos((np.cos(ZO) - np.cos(OP) * np.cos(PZ)) / (np.sin(OP) * np.sin(PZ)))
rightAscension = siderealTime - hourAngle

print("declination = ", declination)
print("rightAscension = ", rightAscension)
