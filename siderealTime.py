import solarNoon
import timeConversions
import datetime
import numpy as np
import math
debug=False

# Takes in a decimal like 12.55 and converts it to a string with format HH:MM:SS
def convertDecimalToTime(value):
    hrValue = math.floor(value)
    minValue = math.floor(60*(value % 1))
    secValue = round((3600*(value % 1)) % 60)
    return f"{hrValue:02d}:{minValue:02d}:{secValue:02d}"

# Takes in two floats, one aware datetime object
# Returns a float for siderealTime in range [0, 24)
def getSiderealTime(latitude, longitude, time):
    # Getting time zone of userTime
    timezone = timeConversions.getTimeZone(latitude, longitude)

    localSolarNoon = solarNoon.calculateSolarNoon(timezone, longitude, time)
    if debug:
        print("Local Solar Noon: ", convertDecimalToTime(localSolarNoon))

    # Using current date to figure out offset from vernal equinox
    vernalEquinox = datetime.datetime(time.year, 3, 20, 9, 46, 0)
    offset = time-vernalEquinox
    vernalOffset = (offset.days + (offset.seconds / 3600 / 24)) / 365.25
    # print("vernalOffset:", vernalOffset)

    # Using current time to figure out offset from solar noon
    currentTime = time.hour + (time.minute / 60)
    solarNoonOffset = (currentTime - localSolarNoon) / 24
    # print("Solar noon offset:", solarNoonOffset)

    # Calculate siderealtime
    siderealTime = 24 * (solarNoonOffset + vernalOffset)# have faith

    if (siderealTime < 0):
        siderealTime += 24
    if (siderealTime >= 24):
        siderealTime -= 24
    if debug:
        print("Sidereal Time:", convertDecimalToTime(siderealTime))

    # Returning siderealTime as radians
    return siderealTime * np.pi / 12
