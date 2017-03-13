#This is the main file

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from IcwLib import *


#loading the external config file


# Definig the bar as segments of geometry
# the formula is for each ssegment
# [[SegmentHeight, SegmentThickness, SegmentLenght, CutoutHeight]]
# Cutout is assumed to be along entire segment lenght

# Single bar 3 segments 2 of them with holes (beggining and end) definition
copperBarGeometry = np.array([[100,10,100,0],[40,10,200,0],[30,10,12.5,10.4],\
[30,10,134,0],[30,10,14,14],[30,10,134-60,0],[30,10,60,0],\
[30,10,12.5,10.4],[100,10,50+280+300,0]])
# end of Bar geometry definition
# print(copperBarGeometry)


# Defining current load
def currentIcw(time):
    if time <= 3.7:
        return 23500
    else:
        return 0

#Defining the analysis parameters
endTime = 60*10
ambientTemp = 20.5

plotSamplingInterval = 10 #in [s]

# Loop for transient analysis
if endTime > 61*60:
    numberOfSamples = 2*endTime
else:
    numberOfSamples = 20*endTime


sampleTime = numberOfSamples / endTime;

if plotSamplingInterval == 0:
    plotTimeStep = 1
else:
    plotTimeStep = int(plotSamplingInterval * sampleTime)  #to simulate the LAB thermocouples data

numberOfSegments = copperBarGeometry.shape[0]

thermalGarray = generateTHermalConductance(copperBarGeometry, 401)
os.system('cls' if os.name == 'nt' else 'clear') # cler console

print('Thermal Conductance Array: ')
print(thermalGarray)

deltaTime = float(endTime) / float(numberOfSamples)

temperatures = np.ones((numberOfSamples, numberOfSegments))*ambientTemp
timeTable = np.zeros(numberOfSamples)

for time in range(1,numberOfSamples,1):
        #progress bar
        printProgressBar(time, numberOfSamples -1, prefix = 'Progress:', \
        suffix = 'Complete', length = 50)

        currentTime = time * deltaTime

        timeTable[time] = currentTime

        temperatures[time] = temperatures[time-1]+ \
        getTempDistr(copperBarGeometry,\
        currentIcw(currentTime), deltaTime, temperatures[time -1] ,\
        ambientTemp, 8920, 385, 3.75 ,thermalGarray, 0.35)
        #barGeometry, Irms, timeStep, startTemp,ambientTemp, density, Cp, baseHTC, thermG, emmisivity

plt.ylabel('Temp [deg C]')
plt.xlabel('time [s]')
plt.grid(1)


#preparing results arrays according to options
timeTable = timeTable[0::plotTimeStep]

#preparing result table for CSV file
myDataArray =[]
myDataArray.append(timeTable)
#Prepareing result table for first row descriptipon
myDataDescription = []
myDataDescription.append('time[s]')



#for i in range(0,numberOfSegments):
for i in [2,4,6,7]:

    plt.plot(timeTable, np.mean(np.array(temperatures)[:,i].reshape(-1,plotTimeStep), axis=1), label="["+str(i+1)+"]")

    myDataArray.append(np.array(np.mean(np.array(temperatures)[:,i].reshape(-1,plotTimeStep), axis=1),))
    myDataDescription.append('Point: '+str(i))


#save data to external CSV file
myDataArray = np.transpose(myDataArray) #transpose data to be in columns
myDataArray = np.vstack((np.array(myDataDescription),myDataArray)) #adding 1st row with description

df = pd.DataFrame(myDataArray)
df.to_csv("./thermalResults.csv")

# Place a legend to the right of this smaller subplot.

plt.legend(bbox_to_anchor=(0.75, 0.95), loc=2, borderaxespad=0.)
drawCuShape(copperBarGeometry, True)
#dipsplay plots
plt.show()
