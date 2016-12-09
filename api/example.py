# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from edge import sobel,mainops
import numpy as np

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

pictureDim = []
imageBuffer = None
root = 0
scatterSettings = []
sendImage = None
sendPart = None
recvImage = []
filename = "earth.jpg"

if rank == 0:
    mainops.info_flag()
    if size < 2:
        print("Operating in singleton mode")
    else:
        message = "Operating in parallel mode using " + str(size) + " processing cores" + '\n'
        print(message)

    imArray = mainops.load_image(filename)

    imageDimensions = imArray[...,0].shape
    imageWaveDepth = imArray[0,0,:].shape[0]

    imageBuffer = np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0]))
    sobelBuffer = np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0]))

    mainops.info_flag()
    print(" %s has %d channels\n" % (filename,imageWaveDepth))

    imageBuffer = mainops.singleton_convertToBlack(imArray)
    pictureDim = imageDimensions

pictureDim = comm.bcast(pictureDim, root)
scatterSettings = mainops.partition(pictureDim,comm)
recvPart = np.getbuffer(np.zeros(scatterSettings[0][rank]))

if rank == 0:
    sendImage = buffer(imageBuffer.reshape((-1,)))
    mainops.info_flag()
    print(" Scattering the image...\n")

comm.Scatterv([sendImage,scatterSettings[0],scatterSettings[1],mpi.DOUBLE], recvPart, root=0)

recvWorker = np.frombuffer(recvPart).reshape((-1,pictureDim[1]))

filenamepart = "part_%d.jpg" % rank
mainops.save_image(recvWorker,filenamepart)

#sobelDistBuffer = sobel.distrib_sobel(imageBuffer,comm,0)

#sobelBuffer = sobel.singleton_sobel(imageBuffer)

#mainops.save_image(sobelBuffer, "teapot_sobel.jpg")

#comm.Gatherv(recvPart.reshape((-1,)),[imageComplete,tuple(sizeArray),tuple(displacement),mpi.INT], root=0)

#if rank == 0:
    #mainops.save_image(imageComplete, "teapot_return.jpg")
