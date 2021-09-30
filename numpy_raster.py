# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:03:23 2020

@author: grox1678
"""

from time import clock
start = clock()
import numpy as np
import arcpy
from arcpy import env
import arcpy.sa as sa
arcpy.CheckOutExtension("Spatial")
env.workspace = r"D:\GIS_Python\data"
env.overwriteOutput = 1


nlcd5 = "nlcd06"
dem5 = 'dem'
trainnlcd = 'train_nlcd'
traindem = 'train_dem'

nlcd5rast = sa.Raster(nlcd5)
dem5rast = sa.Raster(dem5)

nlcd5raster = arcpy.RasterToNumPyArray(nlcd5rast)
dem5raster = arcpy.RasterToNumPyArray(dem5rast)

#find slope
slopedem = arcpy.sa.Slope(dem5)
rastslope = arcpy.RasterToNumPyArray(slopedem)

#boolean output
green = np.where((nlcd5raster>41)&(nlcd5raster<52),1,0);green
agr = np.where((nlcd5raster==82)&(nlcd5raster==81),1,0);agr
water = np.where((nlcd5raster==11),1,0);water
lowintensity = np.where((nlcd5raster==22),1,0);lowintensity


#percentages - moving window
sumArray = np.zeros_like(nlcd5raster)
for row in range(5,nlcd5raster.shape[0]-1):
    for col in range(6,nlcd5raster.shape[1]-1):
    #sets border for moving window
        winSum = 0.0
        #sets boundaries of moving window
        for winRow in range(row-5,row+4):
            for winCol in range(col-6,col+5):
                winSum = winSum + nlcd5raster[winRow,winCol]
        sumArray[row,col] = winSum/99


finalRast = arcpy.NumPyArrayToRaster()