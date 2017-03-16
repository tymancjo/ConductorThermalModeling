#This is the main file

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from IcwLib import *
from geometryLib import *



# Definig the bar as segments of geometry
# the formula is for each ssegment
# [[SegmentHeight, SegmentThickness, SegmentLenght, CutoutHeight]]
# Cutout is assumed to be along entire segment lenght

# Single bar 3 segments 2 of them with holes (beggining and end) definition

#copperBarGeometry = np.array([[30,10,20,0],[30,10,90,0],\
#[30,10,5,10],\
#[30,10,90,0],[30,10,20,0]])

copperBarGeometry = np.array([[30,10,170,0],[30,10,170,0],\
[1,1,1000,0],\
[100,10,72.5,0],[100,10,72.5,0]])
# end of Bar geometry definition
# print(copperBarGeometry)



# Defining current load
def currentIcw(time):
    if time <= 3.7:
        return 0
    else:
        return 0

#Defining the analysis parameters
endTime = 9980
ambientTemp = 200
barStartTemperature = 24.6

plotSamplingInterval = 5 #in [s]

# Loop for transient analysis
if endTime > 61*60:
    numberOfSamples = 2*endTime
else:
    numberOfSamples = 50*endTime
sampleTime = numberOfSamples / endTime;

def mainAnalysis(numerAnalizy, HTC, Emiss):

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

    temperatures = np.ones((numberOfSamples, numberOfSegments))*barStartTemperature
    timeTable = np.zeros(numberOfSamples)

    for time in range(1,numberOfSamples,1):
            #progress bar
            printProgressBar(time, numberOfSamples -1, prefix = 'Progress:', \
            suffix = 'Complete', length = 50)

            currentTime = time * deltaTime

            timeTable[time] = currentTime / 60

            temperatures[time] = temperatures[time-1]+ \
            getTempDistr(copperBarGeometry,\
            currentIcw(currentTime), deltaTime, temperatures[time -1] ,\
            ambientTemp, 8920, 385, HTC ,thermalGarray, Emiss)
            #barGeometry, Irms, timeStep, startTemp,ambientTemp, density, Cp, baseHTC, thermG, emmisivity

    return temperatures


ResultsData = np.array(mainAnalysis('HTC = 25, e=0.2',25,0.2))


plotCurves(timeTable=np.arange(0, 9980, 0.5),dataArray=np.delete(ResultsData,[1,2,4],1),\
plotName='HTC=25.e=0.2',xLabel='time [s]',yLabel='Temperature [degC]',\
curvesLabelArray = ['30x10','100x10'])

#loading the external config file
#external data csv - to use as comarison in plots
srcData = np.array(pd.read_csv('./src/srcData.csv',sep=";"))


plotCurves(timeTable=np.arange(0, 9980, 5),dataArray=srcData,\
plotName='HTC=25.e=0.2',xLabel='time [s]',yLabel='Temperature [degC]',\
curvesLabelArray = ['src30x10','src30x10'])

plt.show()
