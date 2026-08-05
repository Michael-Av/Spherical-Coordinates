import numpy as np

# All variables in radians
def getDistance(userRA, userDec, starRA, starDec):
    distRA = abs(userRA - starRA)
    if distRA > np.pi:
        distRA = 2 * np.pi - distRA

    distDec = abs(userDec - starDec)
    if distDec > np.pi:
        distDec = 2 * np.pi - distDec

    # print("RA distance: ", distRA)
    # print("Dec distance: ", distDec)

    return (distRA**2 + (3*distDec)**2) ** 0.5

def parseEquatorialCoords(line):
    RAhr = float(line[44:46])
    RAmin = float(line[47:49])
    dec = float(line[50:55]) * np.pi / 180

    RA = RAhr * np.pi / 12 + (RAmin * np.pi / 720)
    return [RA, dec]


def findNearestStar(userRA, userDec):
    shortestDist = 20
    closestStar = ""
    with open("Data/stars.txt") as file:
        file.readline()
        for line in file:
            name = line[26:44].strip()
            RA, dec = parseEquatorialCoords(line)

            # print("Right Ascension: ", RA)
            # print("Declination: ", dec)

            thisDist = getDistance(userRA, userDec, RA, dec)
            if thisDist < shortestDist:
                shortestDist = thisDist
                closestStar = name

    return closestStar

def getEquatorialCoords(starName):
    starName = starName.lower()
    with open("Data/stars.txt") as file:
        for line in file:
            name1 = line[:26].strip().lower()
            name2 = line[26:44].strip().lower()
            # print(name1, ", ", name2)
            if starName == name1 or starName == name2:
                print("match found")
                return parseEquatorialCoords(line)

def getAllEquatorialCoords():
    allCoords = []
    with open("Data/stars.txt") as file:
        file.readline()
        for line in file:
            name = line[26:44].strip()
            if not name:
                name = line[:26].strip()
            coords = [name]
            coords.extend(parseEquatorialCoords(line))
            allCoords.append(coords)
    return allCoords