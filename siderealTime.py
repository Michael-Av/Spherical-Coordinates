import solarNoon
import timeConversions
import datetime

latitude = 40.77
longitude = -74

# Getting time zone of userTime
currentTime = datetime.datetime(2025, 9, 12, 18, 23, 0)
timezone = timeConversions.getTimeZone(latitude, longitude)

solarNoon = solarNoon.calculateSolarNoon(timezone, longitude, currentTime)

# Using current date to figure out offset from vernal equinox
vernalEquinox = datetime.datetime(currentTime.year, 3, 20, 0, 0, 0)
vernalOffset = (currentTime - vernalEquinox).days / 365.0
print(vernalOffset)

# Using current time to figure out offset from solar noon
time = currentTime.hour + (currentTime.minute / 60)
solarNoonOffset = (time - solarNoon) / 24
print(solarNoonOffset)

# Calculate siderealtime
siderealTime = 24 * (solarNoonOffset + vernalOffset)
print(siderealTime)

#print(solarNoon)
