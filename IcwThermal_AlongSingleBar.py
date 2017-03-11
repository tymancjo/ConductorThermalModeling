#This is the main file

import numpy as np
import matplotlib.pyplot as plt
from IcwLib import *

# Definig the bar as segments of geometry
# the formula is for each ssegment
# [[SegmentHeight, SegmentThickness, SegmentLenght, CutoutHeight]]
# Cutout is assumed to be along entire segment lenght

# Single bar 3 segments 2 of them with holes (beggining and end) definition
copperBarGeometry = np.array([[100,10,50,0],[30,10,10,0],[30,10,10,10],\
[30,10,145,0],[30,10,10,10],[30,10,145,0],\
[30,10,10,10],[30,10,10,0],[100,10,50,0]])
# end of Bar geometry definition
# print(copperBarGeometry)


# Defining current load
def currentIcw(time):
    if time <= 3:
        return 25e3
    else:
        return 0


# Loop for transient analysis
endTime = 60*10
numberOfSamples = 10*endTime
ambientTemp = 24

numberOfSegments = copperBarGeometry.shape[0]

thermalGarray = generateTHermalConductance(copperBarGeometry, 401)
print(thermalGarray)

deltaTime = float(endTime) / float(numberOfSamples)

temperatures = np.ones((numberOfSamples, numberOfSegments))*ambientTemp
timeTable = np.zeros(numberOfSamples)

for time in range(1,numberOfSamples,1):
        currentTime = time * deltaTime

        timeTable[time] = currentTime

        temperatures[time] = temperatures[time-1]+ \
        getTempDistr(copperBarGeometry,\
        currentIcw(currentTime), deltaTime, temperatures[time -1] ,\
        ambientTemp, 8920, 385, 100,thermalGarray, 0.75)


plt.ylabel('Temp Rise [K]')
plt.xlabel('time [s]')
plt.grid(1)



for i in range(0,numberOfSegments):
    plt.plot(timeTable, np.array(temperatures)[:,i],\
    label="["+str(i+1)+"]")

# Place a legend to the right of this smaller subplot.
plt.legend(bbox_to_anchor=(0.75, 0.95), loc=2, borderaxespad=0.)
drawCuShape(copperBarGeometry)
plt.show()
