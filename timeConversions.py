import timezonefinder
import pytz
import datetime

lati = 43.01
long = -74

# Getting the name of the time zone at latitude and longitude
tzf = timezonefinder.TimezoneFinder()
user_timezone = tzf.timezone_at(lat=lati, lng=long)
#print("Time zone at latitude:", lati, "longitude:", long, "  -- ", user_timezone)

gmtTZ = pytz.timezone('Etc/GMT0');
userTZ = pytz.timezone(user_timezone);

# Getting local and GMT time
time = datetime.datetime.now()
userTime = userTZ.localize(time)
gmtTime = userTime.astimezone(gmtTZ)


# import datetime
# import pytz
#
# # Get a time zone object
# eastern = pytz.timezone('US/Eastern')
#
# # Localize a naive datetime
# naive_dt = datetime.datetime(2024, 3, 21, 10, 0, 0)
# local_dt = eastern.localize(naive_dt)
#
# # Convert to another time zone
# utc_dt = local_dt.astimezone(pytz.utc)
#
# print(f"Naive: {naive_dt}")
# print(f"Local: {local_dt}")
# print(f"UTC: {utc_dt}")
