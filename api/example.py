# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from edge import sobel,blur,sharpen,pixel,mainops
import numpy as np
import socket

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
hostname = socket.gethostname()

pictureDim = []
imageBuffer = None
root = 0
scatterSettings = []
sendImage = None
sendPart = None
resultBuffer = []
filename = "lena.bmp"

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
    resultBuffer = np.getbuffer(np.zeros((imArray[:,0,:].shape[0],imArray[0,:,:].shape[0])))

    mainops.info_flag()
    print(" %s has %d channels\n" % (filename,imageWaveDepth))

    imageBuffer = mainops.singleton_convertToBlack(imArray)
    pictureDim = imageDimensions

    del imArray

pictureDim = comm.bcast(pictureDim, root)
scatterSettings = mainops.partition(pictureDim,comm)
recvPart = np.getbuffer(np.zeros(scatterSettings[0][rank]))

if rank == 0:
    sendImage = buffer(imageBuffer.reshape((-1,)))
    mainops.info_flag()
    print(" Scattering the image...\n")

comm.Scatterv([sendImage,scatterSettings[0],scatterSettings[1],mpi.DOUBLE], recvPart, root=0)

recvWorker = np.frombuffer(recvPart).reshape((-1,pictureDim[1]))
del recvPart
mainops.info_flag()
print(" [%s:%d]: Image download completed\n" % (hostname,rank))

resultWorker = sharpen.sharpen(recvWorker)
resultWorker = pixel.brightness(resultWorker,30)
resultWorker = pixel.contrast(resultWorker,3.5)

comm.Barrier() # Barrier

comm.Gatherv(buffer(resultWorker.reshape((-1,))),[resultBuffer,scatterSettings[0],scatterSettings[1],mpi.DOUBLE], root=0)
mainops.info_flag()
print(" [%s:%d]: Image upload completed\n" % (hostname,rank))

if rank == 0:
    resultImage = np.frombuffer(resultBuffer).reshape((-1,pictureDim[1]))
    del resultBuffer
    mainops.info_flag()
    print(" [%s:%d]: Image reassembly completed\n" % (hostname,rank))
    mainops.save_image(resultImage, "lena_sharpen.png")
