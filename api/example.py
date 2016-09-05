# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from edge import sobel
import numpy as np
import Image

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#lineArray = np.
imArray = sobel.load_image("bottle.jpg")

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

    imageBuffer = sobel.singleton_convertToBlack(imArray)

    sobelBuffer = sobel.singleton_sobel(imageBuffer)

    sobel.save_image(sobelBuffer, "bottle_sobel.jpg")
