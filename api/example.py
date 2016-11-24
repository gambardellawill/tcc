# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from edge import sobel,mainops
import numpy as np
import Image

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
pictureHeight = None

if rank == 0:
    imArray = mainops.load_image("teapot.jpg")

    imageDimensions = imArray[...,0].shape
    imageWaveDepth = imArray[0,0,:].shape[0]

    imageBuffer = np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0]))
    sobelBuffer = np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0]))

    if size < 2:
        print("Operating in singleton mode")
    else:
        message = "Operating in parallel mode using " + str(size) + " processing cores"
        print(message)

    print(imageWaveDepth)
    print(imageBuffer.shape)

    imageBuffer = mainops.singleton_convertToBlack(imArray)

pictureHeight = comm.bcast(imageBuffer.shape[0], root=0)

    #sobelDistBuffer = sobel.distrib_sobel(imageBuffer,comm,0)

    #sobelBuffer = sobel.singleton_sobel(imageBuffer)

    #mainops.save_image(sobelBuffer, "teapot_sobel.jpg")
