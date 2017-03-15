# This is library for geometry analysis and operations
# for the Icw engine
import numpy as np


# Slicer function - for creating more dense segments fro analysis
def slicer(barGeometry, desiredSegmentLenght):
    # Checking number of oryginal segments
    numberOfOrgSegments = len(barGeometry)
    newBarGeometry =[]

    for segment in range(0,numberOfOrgSegments):
        segmentLenght = barGeometry[segment][2]

        if segmentLenght > desiredSegmentLenght:
            # here we do sub segmentation process
            newBarGeometry.append([0,0,0,0])

        else:
            #here we return unchnged segment
            newBarGeometry.append(barGeometry[segment])

    return np.array(newBarGeometry)
