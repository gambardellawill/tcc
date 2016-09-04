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

def singleton_convertToBlack(nArray):
    height = nArray[0,:,:].shape[0]
    width = nArray[:,0,:].shape[0]
    depth = nArray[0,0,:].shape[0]

    bwArray = np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0]))

    for k in range(0,depth):
        bwArray += nArray[...,k]

    bwArray /= 3

    return bwArray

def singleton_sobel(bwArray):
    kernel = np.zeros((3,3))
    print(kernel.shape)

    return bwArray

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#lineArray = np.
imArray = load_image("earth.jpg")

imageDimensions = imArray[...,0].shape
imageWaveDepth = imArray[0,0,:].shape[0]

if rank == 0:
    imageBuffer = np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0]))
    sobelBuffer = np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0]))

    if size < 2:
        print("Operating in singleton mode")
    else:
        message = "Operating in parallel mode using " + str(size) + " processing cores"
        print(message)

    print(imageWaveDepth)
    print(imageBuffer.shape)

    #print(np.ascontiguousarray(imArray[...,rank],dtype=np.uint8).size)

    imageBuffer = singleton_convertToBlack(imArray)

    sobelBuffer = singleton_sobel(imageBuffer)

    for iterator in range(0,(imArray[:,0,:].shape[0])):
        print("Done", iterator)
        comm.Reduce(np.ascontiguousarray(imArray[:,iterator,rank],\
        dtype=np.uint8),np.ascontiguousarray(imageBuffer[:,iterator],\
        dtype=np.uint8), op=mpi.SUM, root=0)


    save_image(imageBuffer, "earth_bw.jpg")

    save_image(sobelBuffer, "earth_sobel.jpg")
