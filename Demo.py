#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo program for Vialux DMD V7000

@author: Arturo Farolfi
"""
import sys
# sys.path.append(r"\pyALP4")
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
bitDepth = 8
images = []


# imgBlack = np.zeros([DMD.nSizeY,DMD.nSizeX])
# imgWhite = np.ones([DMD.nSizeY,DMD.nSizeX])*255
# images.append(imgWhite)
# images.append(imgBlack)

for x in np.arange(1, 20, 1):
    images.append(np.array([ (i%(x*2) > x)*255 for i in range(1024)]*768).reshape( (768, 1024) ))

# imgWhite = np.stack([np.arange(1024)*255/1024]*768)
# images.append(imgStripe)

imgSeq  = np.concatenate([x.ravel() for x in images])
# imgSeq = imgBlack.ravel()

# Allocate the onboard memory for the image sequence
DMD.SeqAlloc(nbImg = len(images), bitDepth = bitDepth)
# # Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)

# # Set image rate to 50 Hz
DMD.SetTiming(illuminationTime = 1000000)

# # Run the sequence in an infinite loop
DMD.Run()

# time.sleep(180)
input("Waiting until Enter...")

# # Stop the sequence display
DMD.Halt()
# # Free the sequence from the onboard memory
DMD.FreeSeq()
# # De-allocate the device
DMD.Free()

