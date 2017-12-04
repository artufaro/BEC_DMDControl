# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:24:57 2017

@author: BEC1
"""

import numpy as np  
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import PIL.Image as IM

imageFile = r"Measurements\Flat_Top1.tif"

img = IM.open(imageFile)

data = np.array(img.convert("L").getdata()).reshape( (img.height, img.width) )

X = np.indices(data.shape)[0]
Y = np.indices(data.shape)[1]

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
ax.plot_surface(X, Y, data)
