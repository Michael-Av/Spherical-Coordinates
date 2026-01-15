import solarNoon
import timeConversions
import datetime
import numpy as np

latitude = 54
longitude = 0

# Takes in two floats, one aware datetime object
# Returns a float for siderealTime in range [0, 24)
def getSiderealTime(latitude, longitude, time):
    # Getting time zone of userTime
    timezone = timeConversions.getTimeZone(latitude, longitude)

    localSolarNoon = solarNoon.calculateSolarNoon(timezone, longitude, time)
    print("localSolarNoon: ", localSolarNoon)

    # Using current date to figure out offset from vernal equinox
    vernalEquinox = datetime.datetime(time.year, 3, 20, 9, 46, 0)
    offset = time-vernalEquinox
    vernalOffset = (offset.days + (offset.seconds / 3600 / 24)) / 365.25
    print("vernalOffset:", vernalOffset)

    # Using current time to figure out offset from solar noon
    currentTime = time.hour + (time.minute / 60)
    solarNoonOffset = (currentTime - localSolarNoon) / 24
    print("Solar noon offset:", solarNoonOffset)

    # Calculate siderealtime
    siderealTime = 24 * (solarNoonOffset + vernalOffset)# have faith

    if (siderealTime < 0):
        siderealTime += 24
    if (siderealTime >= 24):
        siderealTime -= 24
    print("siderealTime:", siderealTime)

    # Returning siderealTime as a fraction of 2 pi
    return siderealTime * np.pi / 12


# getSiderealTime(latitude, longitude, datetime.datetime(2025, 4, 23, 20, 15, 0))
