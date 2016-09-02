# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
import numpy as np
import Image

def save_image(nArray, outputFile):
    imageData = Image.fromarray(np.asarray(np.clip(nArray,0,255), dtype="uint8"), "L")
    imageData.save(outputFile)
    imageData.show()

def load_image(inputFile):
    imageRaw = Image.open(inputFile)
    inputArray = np.asarray(imageRaw)
    return inputArray

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

imArray = load_image("earth.jpg")

print(imArray[...,1].shape)


for iterator in range(0,3):
    save_image(imArray[...,iterator], "earth" + str(iterator)+ ".jpg")


print(rank)
