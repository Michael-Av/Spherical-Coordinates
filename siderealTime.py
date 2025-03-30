import solarNoon
import timeConversions

latitude = 40.77
longitude = -73.98

# Getting time zone of userTime
timezone = timeConversions.getTimeZone(latitude, longitude)
solarNoon = solarNoon.calculateSolarNoon(timezone, longitude)


print(solarNoon)
# print("Local User time            :", userTime)
# print("Local saoTome Solar Noon time:", localsaoTomeNoon)
# print("Local Solar Noon time: %d:%2d" % (solarNoon // 1, (solarNoon % 1) * 60))
