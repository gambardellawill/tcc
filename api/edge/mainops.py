# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from math import *
from PIL import Image
import numpy as np
import kernel
import mainops

def info_flag():
    print("\033[1;37;42m INFO \033[0m")

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

def get_split_lines(imageDimensions,comm):
    nop = float(comm.Get_size())
    nol = float(imageDimensions[0])
    linesArray = []

    remainder = nol%nop

    for rankNumber in range(0,int(nop)):
        if remainder == 0:
            linesArray.append(int(nol/nop))
        elif rankNumber < remainder:
            linesArray.append(int(ceil(nol/nop)))
        else:
            linesArray.append(int(floor(nol/nop)))

    return linesArray

def get_size_tuple(imageDimensions,linesArray,comm):
    sizes = tuple(np.multiply(linesArray,imageDimensions[1]))
    return sizes

def get_displacements_tuple(sizeArray,comm):
    nop = comm.Get_size()
    disp = [0,]

    for p in range(1,nop):
        disp.append(disp[p-1]+sizeArray[p-1])

    return tuple(disp)

def partition(imageDimensions,comm):
    rank = comm.Get_rank()
    sizetup = get_size_tuple(imageDimensions,get_split_lines(imageDimensions,comm),comm)
    disptup = get_displacements_tuple(sizetup,comm)

    #print sizetup
    #print disptup

    return [sizetup,disptup]

def collect():
    return 0
