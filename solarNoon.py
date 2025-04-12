import timeConversions
import datetime

saoTomeLatitude = 0.3376
saoTomeLongitude = 6.7299

def calculateSolarNoon(userTimeZone, userLongitude, time):
    # Getting saoTome information
    saoTomeYear = time.year
    saoTomeMonth = time.month
    saoTomeDay = time.day
    saoTomeHour = 11
    saoTomeMinute = 33
    saoTomeSecond = 0
    saoTomeTimeZone = 'Etc/GMT0'

    saoTomeNoon = saoTomeHour + saoTomeMinute / 60
    saoTomeNoonFormatted = datetime.datetime(saoTomeYear, saoTomeMonth, saoTomeDay, saoTomeHour, saoTomeMinute, saoTomeSecond)
    timezoneOffset = timeConversions.getTimeZoneOffset(saoTomeNoonFormatted, saoTomeTimeZone, userTimeZone)
    #print(timezoneOffset)
    # Using negatives to keep track of west of GMT
    if (timezoneOffset > 12):
        timezoneOffset -= 24
    localsaoTomeNoon = saoTomeNoon + timezoneOffset


    # Using angular distance to determine when solar noon would be for user
    # The localsaoTomeNoon is solar noon for saoTome in the time zone of the user. The solar noon for the user
    # is the solar time for saoTome minus the angular difference in the two place's longitudes

    # Getting angular longitudinal distance from saoTome (between -1 and 1)
    # i.e. How far east (or west if negative) you'd have to walk around the Earth from saoTome to user
    physicalAngularDist = (userLongitude - saoTomeLongitude) / 360
    solarNoon = localsaoTomeNoon - physicalAngularDist * 24

    return solarNoon
