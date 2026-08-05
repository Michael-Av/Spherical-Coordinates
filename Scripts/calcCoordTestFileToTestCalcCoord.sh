#!/usr/bin/bash

# data to test

hrsToRad() {
  echo "($1+$2/60)*3.14159265/12" | bc -l
  # echo "$((($1 + $2 / 60) * 24 / 2 / 3.14159265))" <- no
}

degToRad() {
  echo "($1+$2/60)*3.14159265/180" | bc -l
}

names=('M80' 'a' 'b' 'c')
altitudes=(8.7)
azimuths=(110.9)
latitudes=(44)
longitudes=(17)
times=('2025/04/29/19/19/00')
ras=($(hrsToRad "16" "17"))
decs=($(degToRad "-22" "-58"))

f() {
  maxIndex=$((${#names[@]} - 1))
  for i in $(seq 0 $maxIndex); do
    echo $i
  done
}


f

# echo "$(((5 / 60) * 24 / 2 / 3.14159265))"
latitude=1
longitude=1
altitude=1
azimuth=1
siderealTime=1

# python3 calculateCoordinates.py altitude azimuth latitude siderealTime
