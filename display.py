import matplotlib.pyplot as plt
import numpy as np
PI = np.pi

plt.style.use('dark_background')

def plotVisibleStars(names, altitudes, azimuths):
    names.append("")
    altitudes.append(5*PI/180)
    azimuths.append(0)
    invertedAltitudes = []
    for alt in altitudes:
        invertedAltitudes.append((PI/2 - alt)*180/PI)
    
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    radiiVals = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    tickLabels = ["80\xb0", "70\xb0", "60\xb0", "50\xb0", "40\xb0", "30\xb0", "20\xb0", "10\xb0", "0\xb0"]
    plt.rgrids(radiiVals, labels=tickLabels)
    ax.set_ylim(0,90)

    ax.scatter(azimuths, invertedAltitudes)
    for i in range(len(azimuths)):
        # print(names[i], azimuths[i])
        plt.text(azimuths[i], invertedAltitudes[i], names[i])

    plt.show()