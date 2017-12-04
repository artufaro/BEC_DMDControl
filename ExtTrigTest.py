# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 11:33:53 2017

@author: Arturo Farolfi

DMD with external triggering testing script
"""

import sys
import numpy as np  
import time

if sys.version_info[0] < 3:
    from pyALP4.ALP4 import *
else:
    from pyALP4.ALP4_p3 import *


# Load the Vialux .dll
DMD = ALP4(version = '4.3', libDir = 'C:/Program Files/ALP-4.3/ALP-4.3 API')
# Initialize the device
DMD.Initialize()

# Binary amplitude image (0 or 1)
bitDepth = 1

images = []

for i in range(20):
    img = np.array([(x%20 >= i) *255 for x in range(DMD.nSizeX)]*DMD.nSizeY).reshape([DMD.nSizeY,DMD.nSizeX])
    images.append(img)
#    images.append( np.ones( (768, 1024))*255)
#    images.append( np.zeros( (768, 1024)))
imgSeq  = np.concatenate([x.ravel() for x in images])

# Allocate the onboard memory for the image sequence
DMD.SeqAlloc(nbImg = len(images), bitDepth = bitDepth)

#Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)

#Set slave mode (external trigger)
DMD.ProjControl(ALP_PROJ_MODE, ALP_SLAVE)

#Set image rate to 20 Hz
DMD.SetTiming(pictureTime = 50000)

#invert colors
DMD.ProjControl(ALP_PROJ_INVERSION, 0)

#Run the sequence in an infinite loop
DMD.Run(loop= True)

# time.sleep(180)
input("Waiting until Enter...")

# # Stop the sequence display
DMD.Halt()
# # Free the sequence from the onboard memory
DMD.FreeSeq()
# # De-allocate the device
DMD.Free()

