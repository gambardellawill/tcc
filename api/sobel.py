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

def convert_intensity(nArray): //Not efficient
    pixel =


comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

imageBuffer = numpy.zeros(1)

if rank == 0:
    if size < 2:
        print("Operando em modo singleton")
    else:
        message = "Operando em modo paralelo com " + str(size) + " cores em uso"
        print(message)

    imArray = load_image("earth.jpg")

    imageDimensions = imArray[...,0].shape

    imageWaveDepth = imArray[0,0,:].shape[0]
    print(imageWaveDepth)

    for iterator in range(0,imageWaveDepth):
        comm.Send(imArray[...,iterator], dest=iterator)
        comm.Recv(imageBuffer, source=iterator)
        #save_image(imArray[...,iterator], "earth" + str(iterator)+ ".jpg")

else:

    comm.Recv()
