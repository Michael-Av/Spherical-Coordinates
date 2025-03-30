import numpy as np

PI = np.pi

# +x = north
# +y = west
# +z = up (towards zenith)

# horizontal coordinates
azimuth = PI / 3;
altitude = PI / 4;

# observer location
latitude = PI / 6;

zenithVec = np.array([0, 0, 1])
poleVec = np.array([1, 0, np.sin(latitude)])
objectVec = np.array([np.cos(azimuth), -1 * np.sin(azimuth), np.tan(altitude)])

print("zenith: ", zenithVec)
print("pole: ", poleVec)
print("object: ", objectVec)
