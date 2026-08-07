import Code.calculateCoordinates as coords
import Code.readLeData as rld
import numpy as np
import datetime as dt
import display
import Tests.display3D as display3D
import argparse
import Code.siderealTime as st

PI = np.pi

# alt=45
# azi=0
# rightAscension, declination = coords.calcCelestialCoords(alt*PI/180, azi*PI/180, lat*PI/180, long*PI/180, time)
# nearestStar = rld.findNearestStar(rightAscension, declination)

# print("declination = ", declination*180/PI)
# print("rightAscension = ", rightAscension*12/PI)
# print("ANSWER!!!!", nearestStar)

# rightAscension, declination = rld.getEquatorialCoords("Pollux")
# coords.calcHorizontalCoords(rightAscension, declination, lat*PI/180, long*PI/180, time)

# commandLength = len(sys.argv)

# altitude = float(sys.argv[1])*PI/180
# azimuth = float(sys.argv[2])*PI/180
# # python3 calculateCoordinates.py altitude azimuth latitude longitude
# if commandLength == 5:
# 	lat = float(sys.argv[3])*PI/180
# 	long = float(sys.argv[4])*PI/180
# 	calcCelestialCoords(altitude, azimuth, lat, long)
# # python3 calculateCoordinates.py altitude azimuthHour azimuthMinute latitude longitude
# elif commandLength == 6:
# 	azimuthHr = float(sys.argv[2]) * PI / 12
# 	azimuthMin = float(sys.argv[3]) * PI / 720
# 	lat = float(sys.argv[4])*PI/180
# 	long = float(sys.argv[5])*PI/180
# 	calcCelestialCoords(altitude, azimuthHr + azimuthMin, lat, long)
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
# 	calcCelestialCoords(altitude, azimuth, lat, long)
# else:
# 	print("Command not recognized: try using a correct format L")
# 	exit()

# -- command line arguments --

parser = argparse.ArgumentParser()
parser.add_argument("position", type=float, nargs=2, metavar=("LAT","LONG"), help="Provide the latitude and longitude of the observer")
parser.add_argument("-t", "--time", type=int, nargs='*', help="Provide the time of observance (format year mon day 24hr min sec); omitting higher orders assumes current (deafult now)")
parser.add_argument("-n", "--numStars", type=int, help="Provide the maximum number of stars to display on the map (deafult 25)", default=25)
parser.add_argument("-i", "--identifyStar", type=float, nargs=2, metavar=("AZIMUTH", "ALTITUDE"), help="Provide the azimuth and altitude in degrees of a star to identify")
parser.add_argument("-r", "--trajectory", action='store_true', help="Display trajectory arrows on map")
parser.add_argument("-c", "--constellation", metavar=("CONSTELLATION_NAME"), help="Provide the name of the constellation you want to graph")
parser.add_argument("-l", "--labels", action='store_true', help="Display labels of important stars on map")

args = parser.parse_args()

lat, long = args.position
time = dt.datetime.now()
if (args.time != None):
    for i in range(len(args.time)):
        index = len(args.time) - i
        if index == 6: time = time.replace(year = args.time[i])
        if index == 5: time = time.replace(month = args.time[i])
        if index == 4: time = time.replace(day = args.time[i])
        if index == 3: time = time.replace(hour = args.time[i])
        if index == 2: time = time.replace(minute = args.time[i])
        if index == 1: time = time.replace(second = args.time[i])

siderealTime = st.getSiderealTime(lat*PI/180, long*PI/180, time)

if (args.identifyStar != None): # identify a given star instead of displaying the map
    if (args.trajectory): raise ValueError("--trajectory and --identifyStar flags are incompatible")

    azimuth, altitude = args.identifyStar
    rightAscension, declination = coords.calcCelestialCoords(altitude*PI/180, azimuth*PI/180, lat*PI/180, long*PI/180, time)
    nearestStar = rld.findNearestStar(rightAscension, declination)
    print("You are looking at", nearestStar, "with estimated coordinates (RA, dec) = (", rightAscension * 12/PI, ",", declination * 180/PI, ")")
    exit(0)

constellation=None
if (args.constellation != None):
    constellation = args.constellation
allCoords = rld.getAllEquatorialCoords(constellation)
visibleStarsNames = []
visibleStarsAltitudes = []
visibleStarsAzimuths = []
visibleStarApparentMagnitudes = []
starCount = 0
for coord in allCoords:
    if starCount < args.numStars:
        name, rightAscension, declination, apparentMagnitude = coord
        altitude, azimuth = coords.calcHorizontalCoords(rightAscension, declination, lat*PI/180, long*PI/180, siderealTime)
        print(name, "can be viewed at:\nAltitude:", altitude*180/PI, "\nAzimuth:", azimuth*180/PI, end="\n\n")
        visibleStarsNames.append(name)
        visibleStarsAltitudes.append(altitude)
        visibleStarsAzimuths.append(azimuth)
        visibleStarApparentMagnitudes.append(apparentMagnitude)
        starCount += 1
        if args.trajectory:
            future_altitude, future_azimuth = coords.calcHorizontalCoords(rightAscension, declination, lat*PI/180, long*PI/180, siderealTime + PI/12)
            visibleStarsAltitudes.append(future_altitude)
            visibleStarsAzimuths.append(future_azimuth)

display3D.plotVisibleStars(visibleStarsNames, visibleStarsAltitudes, visibleStarsAzimuths, visibleStarApparentMagnitudes, args.labels)
        