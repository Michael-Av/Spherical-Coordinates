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
    RAhr = float(line[38:40])
    RAmin = float(line[41:43])
    RAsec = float(line[44:48])

    DECsign = line[49]
    DEChr = float(line[50:52])
    DECmin = float(line[53:55])
    DECsec = float(line[56:58])

    ra = (np.pi/12)*(RAhr + (RAmin/60) + (RAsec/3600))
    dec = (np.pi/180)*(DEChr + (DECmin/60) + (DECsec/3600))
    if DECsign == "-":
        dec = -dec
    return [ra, dec]

def parseStarName(line):
    namesFile = open("Data/stars-names.dat")
    brightStarCatalogNumber = int(line[0:4].strip())
    for line in namesFile:
        currBrightStarCatalogNumber = int(line[0:4].strip())
        if brightStarCatalogNumber == currBrightStarCatalogNumber:
            name = line[6:].strip()
            namesFile.close()
            return name
    # Otherwise the star doesn't have a common name, return scientific name
    scientificName = line[17:25]
    namesFile.close()
    return scientificName

def parseStarConstellation(line):
    return line[22:25]

def parseStarApparentMagnitude(line):
    return float(line[171:176].strip())

def findNearestStar(userRA, userDec):
    shortestDist = 20
    closestStar = ""
    with open("Data/stars-catalog.dat") as file:
        for line in file:
            ra, dec = parseEquatorialCoords(line)
            # print("Right Ascension: ", ra)
            # print("Declination: ", dec)

            thisDist = getDistance(userRA, userDec, ra, dec)
            if thisDist < shortestDist:
                shortestDist = thisDist
                closestStar = parseStarName(line)
    return closestStar

def getEquatorialCoords(starName):
    brightStarCatalogNumber = -1
    with open("Data/stars-names.dat") as file:
        for line in file:
            currName = line[6:].strip()
            if currName.lower() == starName.lower():
                brightStarCatalogNumber = int(line[0:4].strip())
    if brightStarCatalogNumber == -1:   # No common star matched the name
        print("No star found with name", starName)
        return None

    with open("Data/stars-catalog.dat") as file:
        for line in file:
            currBrightStarCatalogNumber = int(line[0:4].strip())
            if brightStarCatalogNumber == currBrightStarCatalogNumber:
                return parseEquatorialCoords(line)

    print("No star found with catalog number", brightStarCatalogNumber)
    return None

def getAllEquatorialCoords(constellation=None):
    allCoords = []
    with open("Data/stars-catalog.dat") as file:
        for line in file:
            currConstellation=parseStarConstellation(line)
            if constellation==None or constellation.lower() == currConstellation.lower():
                coords = [parseStarName(line)]
                coords.extend(parseEquatorialCoords(line))
                coords.append(parseStarApparentMagnitude(line))
                allCoords.append(coords)
    return allCoords