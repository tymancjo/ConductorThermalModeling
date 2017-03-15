#This is the main file

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from IcwLib import *
from geometryLib import *

#loading the external config file


# Definig the bar as segments of geometry
# the formula is for each ssegment
# [[SegmentHeight, SegmentThickness, SegmentLenght, CutoutHeight]]
# Cutout is assumed to be along entire segment lenght

# Single bar 3 segments 2 of them with holes (beggining and end) definition
copperBarGeometry = np.array([[30,10,20,0],[30,10,20,0],[30,10,20,0],[30,10,20,0],[30,10,20,0],\
[30,10,2,10],[30,10,2,10],[30,10,2,10],[30,10,2,10],[30,10,2,10],\
[30,10,20,0],[30,10,20,0],[30,10,20,0],[30,10,20,0],[30,10,20,0]])
# end of Bar geometry definition
print(copperBarGeometry)

copperBarGeometry = slicer(copperBarGeometry, 5)
print(copperBarGeometry)
