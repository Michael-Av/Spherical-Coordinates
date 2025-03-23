import timezonefinder
import pytz
import datetime

# Latitude and longitude can be any number between -180.0 and 180.0
# Returns the name of the timezone at latitude and longitude
def getTimeZone(latitude, longitude):
    tzf = timezonefinder.TimezoneFinder()
    user_timezone = tzf.timezone_at(lat=latitude, lng=longitude)
    #print("Time zone at latitude:", lati, "longitude:", long, "  -- ", user_timezone)
    return user_timezone


# time is an aware datetime object, user_timezone is the name of a timezone (i.e. 'Asia/Kolkata')
# Returns the offset of user's time from GMT (can be from -24.0 to 24.0)
def getTimeZoneOffset(time, initial_timezone, final_timezone):
    tz1 = pytz.timezone(initial_timezone);
    tz2 = pytz.timezone(final_timezone);

    gmtOffset1 = tz1.utcoffset(time)
    gmtOffset2 = tz2.utcoffset(time)

    timeDifference = (gmtOffset2 - gmtOffset1).seconds / 3600.0
    return timeDifference

# time is a naive datetime object, initial_timezone is the name (i.e. 'Asia/Kolkata') of the
#    timezone you are in and final_timezone is the name of the timezone you want the returned time to be in
# Returns the offset of user's time from GMT (can be from -24.0 to 24.0)
def changeTimeZone(time, initial_timezone, final_timezone):
    finalTZ = pytz.timezone(final_timezone);
    initialTZ = pytz.timezone(initial_timezone);

    initTime = initialTZ.localize(time)
    finalTime = initTime.astimezone(finalTZ)

    return finalTime

def localize(time, timezone):
    tz = pytz.timezone(timezone)
    return tz.localize(time)
