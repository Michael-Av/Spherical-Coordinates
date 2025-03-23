import timeConversions
import datetime

quitoLatitude = -0.22
quitoLongitude = -78.5
userLatitude = -34
userLongitude = 18.4

# Getting current time, user time zone
time = datetime.datetime(2025, 3, 23, 5, 56, 0)
userTimeZone = timeConversions.getTimeZone(userLatitude, userLongitude)
print(userTimeZone)
userTime = timeConversions.localize(time, userTimeZone)

# Creating quitoSolarNoon time, converting to user's local time zone
quitoYear = 2025
quitoMonth = 3
quitoDay = 23
quitoHour = 12
quitoMinute = 20
quitoSecond = 0
quitoNoonZone = 'America/Panama'

quitoNoon = quitoHour + quitoMinute / 60
quitoNoonFormatted = datetime.datetime(quitoYear, quitoMonth, quitoDay, quitoHour, quitoMinute, quitoSecond)
localQuitoNoon = quitoNoon + timeConversions.getTimeZoneOffset(quitoNoonFormatted, quitoNoonZone, userTimeZone)

# Using angular distance to determine when solar noon would be for user
# The localquitoNoon is solar noon for Quito in the time zone of the user. The solar noon for the user
# is the solar time for Quito minus the angular difference in the two place's longitudes

# Getting angular longitudinal distance from Quito (between -1 and 1)
# i.e. How far east (or west if negative) you'd have to walk around the Earth from Quito to user
physicalAngularDist = (userLongitude - quitoLongitude) / 360
solarNoon = localQuitoNoon - physicalAngularDist * 24


print("Local User time            :", userTime)
print("Local Quito Solar Noon time:", localQuitoNoon)
print("Local Solar Noon time: %d:%2d" % (solarNoon // 1, (solarNoon % 1) * 60))
