#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo program for Vialux DMD V7000

@author: Arturo Farolfi
"""
import sys
# sys.path.append(r"\pyALP4")
import os
import numpy as np  
import time
from PIL import Image

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

for root, dirs, files in os.walk("./Images"):
    print("found: ", len(files), " files") 
    for f in files:
        if f[-4:]==".bmp":
            print("found: " +os.path.join(root, f))
            IM = Image.open(os.path.join(root, f))
            images.append( np.array(IM.getdata()).reshape( (768, 1024) ) )
        elif f[-4:]==".npy":
            print("found: " +os.path.join(root, f))
            images.append(np.load(os.path.join(root, f)).reshape( (768, 1024) ))
        else:
            print("Not used: " + os.path.join(root, f))
    

imgSeq  = np.concatenate([x.ravel() for x in images])
# imgSeq = imgBlack.ravel()

# Allocate the onboard memory for the image sequence
DMD.SeqAlloc(nbImg = len(images), bitDepth = bitDepth)
# # Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)

#Set Illumination Time 1s
DMD.SetTiming(illuminationTime = 1000000)

#Set External triggering
# DMD.ProjControl(ALP_PROJ_MODE, ALP_SLAVE) 
##DMD.ProjControl(ALP_PROJ_STEP, ALP_LEVEL_LOW)

##Run the sequence in an infinite loop
DMD.Run(loop = True)

# time.sleep(30)
input("Waiting until Enter...")

# # Stop the sequence display
DMD.Halt()
# # Free the sequence from the onboard memory
DMD.FreeSeq()
# # De-allocate the device
DMD.Free()

