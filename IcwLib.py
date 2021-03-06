# This is the library file
import numpy as np
import matplotlib.pyplot as plt

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

#Defining fuction to draw copperbar shape
def drawCuShape(barGeometry, isLabConnect):

    numberOfSegments = barGeometry.shape[0]
    #checking for max bar height in all segments
    #and set the center of bar position y
    centerY = np.max(barGeometry, axis=0)[0]/2

    currentX = 0
    plt.figure(figsize=(12,4))

    for i in range(0,numberOfSegments,1):
        if i== 0 or i==numberOfSegments-1:
            colourOfBar = '#c46f1b'
            segmentLabel = "LAB["+str(i)+"]"
        else:
            colourOfBar = '#f49b42'
            segmentLabel = "["+str(i)+"]"

        # Ploting main coppershape of the segment
        currentY = centerY-barGeometry[i, 0]/2
        segment = plt.Rectangle((currentX, currentY),barGeometry[i, 2]\
        ,barGeometry[i, 0], fc=colourOfBar, linestyle='dashed',\
        edgecolor='grey')

        plt.gca().add_patch(segment)

        #adding text
        plt.text(currentX + barGeometry[i, 2]/2 -5 , \
        currentY + barGeometry[i, 0]/2 -3 ,segmentLabel)

        if barGeometry[i, 3] != 0:
            # Drawing the hole in segment
            hole = plt.Rectangle((currentX, \
            currentY+(barGeometry[i, 0]/2)-(barGeometry[i, 3]/2)),\
            barGeometry[i, 2],barGeometry[i, 3], fc='w')
            plt.gca().add_patch(hole)

        currentX += barGeometry[i, 2]

    #print("Copperbar geometry visualisation")
    plt.axis('scaled')
    #plt.show()


def crossSection(barSegmentArray):
    #cross section = (H-otw)*w
    return ((barSegmentArray[0] - barSegmentArray[3])*barSegmentArray[1])*1e-6

# Calulation of power losses
# the idea is to do it segment by segment applaying
# to subrutine the cross section definition
def powerLosses(xSec,Irms,temp,cond20C, thermRcoef):

    #analysis of xSec array
    #getting data from array
    heightBar = xSec[0]*1e-3
    lenghtBar = xSec[2]*1e-3
    thickBar  = xSec[1]*1e-3
    cutoutBar = xSec[3]*1e-3

    condAtTemp = cond20C / (1 + thermRcoef*(temp - 20))

    activeCrossSection = crossSection(xSec)
    Rdc = lenghtBar/(activeCrossSection * condAtTemp)
    return 1*Rdc * Irms**2

def copperCp(temperatureCu):
    return 423.28-45.089*np.exp(-1*temperatureCu/192.82)

def htc(temp, tempAmb, initialHTC):
    return 0.1*initialHTC*(temp - tempAmb)**0.25


def generateTHermalConductance(barGeometry, thermalCOnduction):
    numberOfSegments = barGeometry.shape[0]
    thermG = np.zeros(numberOfSegments -1)

    for i in range(0,numberOfSegments -1, 1):
        #half lenght of this section thermal resistance
        thR1 = 0.5*barGeometry[i][2]*1e-3/ \
        (crossSection(barGeometry[i])*thermalCOnduction)
        #half lenght of next section thermal resistance
        thR1 += 0.5*barGeometry[i+1][2]*1e-3/ \
        (crossSection(barGeometry[i+1])*thermalCOnduction)
        thermG[i] = 1/thR1

    return thermG

#Defining function for temperature rise calculations
def getTempDistr(barGeometry, Irms, timeStep, startTemp,\
                ambientTemp, density, Cp, baseHTC, thermG, emmisivity):

    numberOfSegments = barGeometry.shape[0]
    segmentTemperatureRise = np.zeros(numberOfSegments)

    # First loop over segments - calculating temp rise from srcs
    # minus convection and conduction from previous timestep tepratures
    for i in range (0, numberOfSegments, 1):
        #getting data from array
        heightBar = barGeometry[i][0]*1e-3
        lenghtBar = barGeometry[i][2]*1e-3
        thickBar  = barGeometry[i][1]*1e-3
        cutoutBar = barGeometry[i][3]*1e-3

        segmentVolume = (heightBar - cutoutBar) * thickBar * lenghtBar
        segmentMass = segmentVolume * density
        barArea = lenghtBar * (2 * ((heightBar - cutoutBar)+ thickBar))

        #Thermal conduction based on the previous step tmeperatures
        if i>0 and i<numberOfSegments-1:
            thermalCOnduction = ((startTemp[i]-startTemp[i-1])*thermG[i-1]+\
            (startTemp[i]-startTemp[i+1])*thermG[i])
        elif i==0:
            thermalCOnduction = ((startTemp[i]-startTemp[i+1]))*thermG[i]
        else:
            thermalCOnduction = ((startTemp[i]-startTemp[i-1]))*thermG[i-1]

        stBoltzConst = 5.6703e-8
        thermalRadiation = stBoltzConst * barArea * emmisivity\
        * ((startTemp[i]+273.15)**4-(ambientTemp+273.15)**4)

        thermalConvection = htc(startTemp[i],ambientTemp,baseHTC) \
        * barArea*(startTemp[i]-ambientTemp)

        segmentTemperatureRise[i] = (powerLosses(barGeometry[i], \
        Irms, startTemp[i], 58e6, 3.9e-3) \
        - thermalConvection\
        - thermalCOnduction - thermalRadiation) \
        * timeStep / (segmentMass * copperCp(startTemp[i]))

    return segmentTemperatureRise
