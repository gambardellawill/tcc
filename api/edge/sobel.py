# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from math import pow,sqrt
import numpy as np
import Image
import kernel
import mainops

def singleton_sobel(bwArray):
    sobelKernel = np.zeros((3,3))

    height = bwArray.shape[0]
    width = bwArray.shape[1]

    xOperator = np.array([
    [-1,0,1],[-2,0,2],[-1,0,1]
    ])

    yOperator = np.array([
    [-1,-2,-1],[0,0,0],[1,2,1]
    ])

    sobelArray = np.zeros((height,width))

    for row in range(0,height):

        if row == 0:    #Tratamento das bordas
            rowUp = row
            rowDown = row+1
        elif row == height-1:
            rowUp = row-1
            rowDown = row
        else:
            rowUp = row-1
            rowDown = row+1

        for column in range(0,width):

            if column == 0: #Tratamento das bordas
                colLeft = column
                colRight = column+1
            elif column == width-1:
                colLeft = column-1
                colRight = column
            else:
                colLeft = column-1
                colRight = column+1

            inputKernel = np.array([\
            [bwArray[rowUp,colLeft],bwArray[rowUp,column],bwArray[rowUp,colRight]],
            [bwArray[row,colLeft],bwArray[row,column],bwArray[row,colRight]],
            [bwArray[rowDown,colLeft],bwArray[rowDown,column],bwArray[rowDown,colRight]]\
            ])

            xAxisDiff = kernel.kernel_operator(inputKernel,xOperator)
            yAxisDiff = kernel.kernel_operator(inputKernel,yOperator)

            sobelArray[row,column] = sqrt(
                pow(xAxisDiff,2)+pow(yAxisDiff,2)
                )

    return sobelArray

def distrib_sobel(bwArray,comm,root):
    if comm.Get_rank() == root:
        sobelKernel = np.zeros((3,3))

        height = bwArray.shape[0]
        width = bwArray.shape[1]

        sobelArray = np.zeros((height,width))

    xOperator = np.array([
    [-1,0,1],[-2,0,2],[-1,0,1]
    ])

    yOperator = np.array([
    [-1,-2,-1],[0,0,0],[1,2,1]
    ])

    return sobelArray
