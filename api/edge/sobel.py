# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
import numpy as np
import Image
import kernel

def save_image(nArray, outputFile):
    imageData = Image.fromarray(np.asarray(np.clip(nArray,0,255), dtype="uint8"), "L")
    imageData.save(outputFile)
    imageData.show()

def load_image(inputFile):
    imageRaw = Image.open(inputFile)
    inputArray = np.asarray(imageRaw)
    return inputArray

def singleton_convertToBlack(nArray):
    height = nArray[0,:,:].shape[0]
    width = nArray[:,0,:].shape[0]
    depth = nArray[0,0,:].shape[0]

    bwArray = np.zeros((width,height))

    for k in range(0,depth):
        bwArray += nArray[...,k]

    bwArray /= 3

    return bwArray

def singleton_sobel(bwArray):
    sobelKernel = np.zeros((3,3))

    height = bwArray.shape[0]
    width = bwArray.shape[1]

    sobelArray = np.zeros((height,width))

    for row in range(0,height):
        for column in range(0,width):
            pixel = bwArray[row,column]
            

    return sobelArray
