# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from math import pow,sqrt
import numpy as np
import Image
import kernel
import mainops

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

def set_array_size(imageHeight,comm):
    nop = float(comm.Get_size())
    sequenceSize = float(imageHeight)
    rankNumber = comm.Get_rank()

    remainder = sequenceSize%nop

    if remainder == 0:
        return sequenceSize/nop
    elif rankNumber < remainder:
        return math.ceil(sequenceSize/nop)
    else:
        return math.floor(sequenceSize/nop)

def lines_to_send(bwArray,numberOfLines,comm):
    nop = float(comm.Get_size())
    rankNumber = comm.Get_rank()
    lines = []

    width = bwArray.shape[1]

    for iterate in range(0,numberOfLines):
        if iterate == 0:
            lineNumber.append(rankNumber)
        else:
            lineNumber.append(rankNumber*iterate + nop)

    return lines
