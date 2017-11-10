#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo program for Vialux DMD V7000

@author: Arturo Farolfi
"""
# import sys
# sys.path.append(r"\pyALP4")
import numpy as np  
from pyALP4.ALP4 import *
import time

# Load the Vialux .dll
DMD = ALP4(version = '4.3', libDir = 'C:/Program Files/ALP-4.3/ALP-4.3 API')
# Initialize the device
DMD.Initialize()

# Binary amplitude image (0 or 1)
bitDepth = 1    
imgBlack = np.zeros([DMD.nSizeY,DMD.nSizeX])
imgWhite = np.ones([DMD.nSizeY,DMD.nSizeX])*(2**8-1)
imgSeq  = np.concatenate([imgBlack.ravel(),imgWhite.ravel()])

# Allocate the onboard memory for the image sequence
DMD.SeqAlloc(nbImg = 2, bitDepth = bitDepth)
# # Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)
# # Set image rate to 50 Hz
# DMD.SetTiming(illuminationTime = 200000)

# # Run the sequence in an infinite loop
# DMD.Run()

# time.sleep(10)

# # Stop the sequence display
# DMD.Halt()
# # Free the sequence from the onboard memory
# DMD.FreeSeq()
# # De-allocate the device
# DMD.Free()

