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

def findNearestStar(userRA, userDec):
    shortestDist = 20
    closestStar = ""
    with open("stars.txt") as file:
        for line in file:
            name = line[26:44].strip()
            RAhr = float(line[44:46])
            RAmin = float(line[47:49])
            dec = float(line[50:55]) * np.pi / 180

            RA = RAhr * np.pi / 12 + (RAmin * np.pi / 720)

            # print("Right Ascension: ", RA)
            # print("Declination: ", dec)

          

            thisDist = getDistance(userRA, userDec, RA, dec)
            if thisDist < shortestDist:
                shortestDist = thisDist
                closestStar = name

    return closestStar
