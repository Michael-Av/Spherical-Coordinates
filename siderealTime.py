import solarNoon
import timeConversions
import datetime

latitude = 40.77
longitude = -73.98

# Getting time zone of userTime
currentTime = datetime.datetime.now()
timezone = timeConversions.getTimeZone(latitude, longitude)

solarNoon = solarNoon.calculateSolarNoon(timezone, longitude, currentTime)

# Using current date to figure out offset from vernal equinox
vernalOffset = (currentTime.month - 3) + ((currentTime.day - 20) / 30)
vernalOffset /= 12
print(vernalOffset)

# Using current time to figure out offset from solar noon
time = currentTime.hour + (currentTime.minute / 60)
solarNoonOffset = (time - solarNoon) / 24
print(solarNoonOffset)

# Calculate siderealtime
siderealTime = 24 * (solarNoonOffset - vernalOffset)
print(siderealTime)

#print(solarNoon)
