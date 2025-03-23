import solarNoon
import timeConversions

latitude = 48.86
longitude = 2.35

# Getting time zone of userTime
timezone = timeConversions.getTimeZone(latitude, longitude)
solarNoon = solarNoon.calculateSolarNoon(timezone, longitude)


print(solarNoon)
# print("Local User time            :", userTime)
# print("Local saoTome Solar Noon time:", localsaoTomeNoon)
# print("Local Solar Noon time: %d:%2d" % (solarNoon // 1, (solarNoon % 1) * 60))
