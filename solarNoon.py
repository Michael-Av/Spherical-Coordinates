import timeConversions
import datetime
import numpy as np

saoTomeLatitude = 0.3376 * np.pi / 180
saoTomeLongitude = 6.7299 * np.pi / 180

def getSaoTomeSolarNoon(userLocalTime):
    with open("dataTable.txt", "r") as file:
        # Each year is approximately 365 + 13 lines in the data table.
        # Thus I will skip ahead by 375 * how many years since 2025 to decrease the runtime
        linesToSkip = 375 * (userLocalTime.year - 2025)
        for i in range(linesToSkip):
            file.readline()

        # Now we should be close to or equal to the correct year in the data table
        # Getting to the correct year in the datatable
        line = file.readline()
        while ((not (str(userLocalTime.year) in line)) and line):
            line = file.readline()

        # Getting to the correct month in the datatable
        while ((not (("-" + str(userLocalTime.month) + "-") in line)) and line):
            line = file.readline()

        # Getting to the correct day in the datatable
        for i in range(userLocalTime.day - 1):
            file.readline()

        solarNoon = file.readline()
        print("sao tome solar noon:", solarNoon)
        return solarNoon[0:5]

def calculateSolarNoon(userTimeZone, userLongitude, time):
    # Getting saoTome information
    saoTomeYear = time.year
    saoTomeMonth = time.month
    saoTomeDay = time.day
    saoTomeSecond = 0
    saoTomeTimeZone = 'Etc/GMT0'
    # Grabbing hour and minute from data table
    saoTomeSN = getSaoTomeSolarNoon(time)
    saoTomeHour = int(saoTomeSN.split(':')[0])
    saoTomeMinute = int(saoTomeSN.split(':')[1])

    saoTomeNoon = saoTomeHour + saoTomeMinute / 60
    saoTomeNoonFormatted = datetime.datetime(saoTomeYear, saoTomeMonth, saoTomeDay, saoTomeHour, saoTomeMinute, saoTomeSecond)
    timezoneOffset = timeConversions.getTimeZoneOffset(saoTomeNoonFormatted, saoTomeTimeZone, userTimeZone)
    #print(timezoneOffset)
    # Using negatives to keep track of west of GMT
    if (timezoneOffset > 12):
        timezoneOffset -= 24
    localsaoTomeNoon = saoTomeNoon + timezoneOffset
    #print("GMT: ",saoTomeNoon)
    #print("NEWYORK: ",localsaoTomeNoon)


    # Using angular distance to determine when solar noon would be for user
    # The localsaoTomeNoon is solar noon for saoTome in the time zone of the user. The solar noon for the user
    # is the solar time for saoTome minus the angular difference in the two place's longitudes

    # Getting angular longitudinal distance from saoTome (between -1 and 1)
    # i.e. How far east (or west if negative) you'd have to walk around the Earth from saoTome to user
    # print("userLongitude:", userLongitude)
    # print("saoTomeLongitude:", saoTomeLongitude)
    physicalAngularDist = (userLongitude - saoTomeLongitude) * (12 / np.pi)
    #print("physicalAngularDist:", physicalAngularDist)
    solarNoon = localsaoTomeNoon - physicalAngularDist

    return solarNoon
