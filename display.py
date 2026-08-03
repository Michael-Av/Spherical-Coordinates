import matplotlib.pyplot as plt
import numpy as np
PI = np.pi

plt.style.use('dark_background')

# if 2 * len(names) = len(altitudes) = len(azimuths), then trajectories are to be plotted
def plotVisibleStars(names, altitudes, azimuths):
    # names.append("")
    # altitudes.append(5*PI/180)
    # azimuths.append(0)
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

    if (2 * len(names) == len(altitudes)): # trajectorie
        ax.scatter(azimuths[::2], invertedAltitudes[::2])
        index = 0
        while index < len(names):
            if (names[index] == 'Polaris'): index += 1 # manually override drawing trajectory for Polaris
            start = (azimuths[2*index], invertedAltitudes[2*index])
            end = (azimuths[2*index+1], invertedAltitudes[2*index+1])
            ax.annotate('', xy=end, xytext=start, xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="->", color="white", lw=2))
            index += 1
        for i in range(len(names)):
            plt.text(azimuths[2*i], invertedAltitudes[2*i], names[i])
    else:
        ax.scatter(azimuths, invertedAltitudes)
        for i in range(len(azimuths)):
            plt.text(azimuths[i], invertedAltitudes[i], names[i])

    plt.show()