#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo program for Vialux DMD V7000

@author: Arturo Farolfi

accepted image formats:
     -bmp with same resolution as chip
     -npy with shape (DMD.nSizeY, DMD.nSizeX) 

images must be a numbered sequence from 000 to <999, imgFormat must contains ***
where the numbers are.
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

#Variables
imgFormat = "Image_***.bmp" # "***" = numbered sequence from 000
imgRoot = "./Images"
illTime = 10e3 #usec

# Load the Vialux .dll
DMD = ALP4(version = '4.3', libDir = 'C:/Program Files/ALP-4.3/ALP-4.3 API')
# Initialize the device
DMD.Initialize()










# Binary amplitude image (0 or 1)
bitDepth = 8
images = []

imgNameTest = imgFormat.split("***")
counter = 0

if imgNameTest[1][-4:] == ".bmp":
    for i in range(1000):
        try:
            imgName = imgNameTest[0]+"%03i"%i+imgNameTest[1]
            IM = Image.open(os.path.join(imgRoot, imgName))
            images.append( np.array(IM.getdata()).reshape( (768, 1024) ) )
        
        except:
            print("found %i files"%i )
            break

if imgNameTest[1][-4:] == ".npy":
    for i in range(1000):
        try:
            imgName = imgNameTest[0]+"%03i"%i+imgNameTest[1]
            IM = np.load(os.path.join(imgRoot, imgName))
            if IM.shape == (DMD.nSizeY,DMD.nSizeX):
                images.append(IM.reshape( (768, 1024) ) )
            else: 
                print("Skipped for wrong shape: " + imgName )
        
        except:
            print("found %i files"%i )
            break

"""
for root, dirs, files in os.walk(imgRoot):
    print("found: ", len(files), " files") 
    for f in files:
        if f[:len(imgNameTest[0])]== imgNameTest[0] and \
            f[-len(imgNameTest[1]):] == imgNameTest[1] and \
            len(f) == len(imgFormat):
            
            print("found: " +os.path.join(root, f))
            IM = Image.open(os.path.join(root, f))
            images.append( np.array(IM.getdata()).reshape( (768, 1024) ) )
        
        else:
            print("Invalid Format: " + os.path.join(root, f))
    
"""
imgSeq  = np.concatenate([x.ravel() for x in images])
# imgSeq = imgBlack.ravel()

# Allocate the onboard memory for the image sequence
DMD.SeqAlloc(nbImg = len(images), bitDepth = bitDepth)
# # Send the image sequence as a 1D list/array/numpy array
DMD.SeqPut(imgData = imgSeq)

#invert colors
DMD.ProjControl(ALP_PROJ_INVERSION, 1)

#Set Illumination Time 1s
DMD.SetTiming(illuminationTime = int(illTime))

#Set External triggering
# DMD.ProjControl(ALP_PROJ_MODE, ALP_SLAVE) 
# DMD.ProjControl(ALP_PROJ_STEP, ALP_LEVEL_LOW)

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

