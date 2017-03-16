#This is the main file

import numpy as np
import matplotlib.pyplot as plt
#import os
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






ResultsData = np.array(mainAnalysis(analysisName='First Study',geometryArray=copperBarGeometry,\
timeArray=np.arange(0, 9980, 5), currentArray=np.ones(9980*2)*0, HTC=25, Emiss=0.2,\
ambientTemp=200, barStartTemperature=25,\
thermalConductivity=401, materialDensity=8920, materialCp=385))


plotCurves(timeTable=np.arange(0, 9980, 5),dataArray=np.delete(ResultsData,[1,2,4],1),\
plotName='HTC=25.e=0.2',xLabel='time [s]',yLabel='Temperature [degC]',\
curvesLabelArray = ['30x10','100x10'])

#loading the external config file
#external data csv - to use as comarison in plots
srcData = np.array(pd.read_csv('./src/srcData.csv',sep=";"))


plotCurves(timeTable=np.arange(0, 9980, 5),dataArray=srcData,\
plotName='HTC=25.e=0.2',xLabel='time [s]',yLabel='Temperature [degC]',\
curvesLabelArray = ['src30x10','src30x10'])

plt.show()
