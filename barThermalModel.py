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
def currentValue(time):
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

def mainAnalysis(analysisName,geometryArray,timeArray, HTC, Emiss,\
thermalConductivity,materialDensity,materialCp):

    print('Starting analysis: '+ str(analysisName))

    #Getting the thermal conductivity array for given shape
    thermalGarray = generateTHermalConductance(geometryArray, thermalConductivity)

    numberOfSegments = geometryArray.shape[0]

    deltaTime = timeArray[1]-timeArray[0] # getting the delta time base on the timeArray
    numberOfSamples = timeArray.size

    # Setting the initial temperatures for segments
    temperatures = np.ones((numberOfSamples, numberOfSegments))*barStartTemperature

    calculationStep = 1 #just the counter reset
    for time in timeArray[1:]:
            #progress bar
            printProgressBar(calculationStep, numberOfSamples -1, prefix = 'Progress:', \
            suffix = 'Complete', length = 50)

            #currentTime = time * deltaTime
            currentTime = time

            temperatures[calculationStep] = temperatures[calculationStep-1]+ \
            getTempDistr(geometryArray,\
            currentValue(currentTime), deltaTime, temperatures[calculationStep -1] ,\
            ambientTemp, materialDensity, materialCp, HTC ,thermalGarray, Emiss)
            #barGeometry, Irms, timeStep, startTemp,ambientTemp, density, Cp, baseHTC, thermG, emmisivity

            calculationStep += 1

    return temperatures


ResultsData = np.array(mainAnalysis(analysisName='First Study',geometryArray=copperBarGeometry,\
timeArray=np.arange(0, 9980, 0.5), HTC=25, Emiss=0.2,\
thermalConductivity=401, materialDensity=8920, materialCp=385))


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
