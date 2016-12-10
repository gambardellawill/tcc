# *-* coding: utf-8 -*-

import numpy as np

def kernel_operator(inputop, kernelop):
    opbuffer = np.zeros((kernelop.shape[0],kernelop.shape[1]))

    opbuffer = np.multiply(inputop,kernelop)
    pixel = np.sum(opbuffer).astype(int)
    pixel = pixel // 9
    
    return pixel

def get_kernel_coords(height,width,row,column):
    bwkernel = []

    for y in range(0,3):
        yint = row-1+y
        if yint <= 0:
            ycoord = 0
        elif yint >= height:
            ycoord = height-1
        else:
            ycoord = yint

        for x in range(0,3):
            xint = column-1+x
            if xint <= 0:
                xcoord = 0
            elif xint >= width:
                xcoord = width-1
            else:
                xcoord = xint

            bwkernel.append((ycoord,xcoord))

    return bwkernel

def kernel_scan(bwArray,kernelMatrix):
    height = bwArray.shape[0]
    width = bwArray.shape[1]
    resultArray = np.zeros((height,width))

    for row in range(0,height):
        print("Row %d of %d is complete" % (row,height))
        for column in range(0,width):
            ikc = get_kernel_coords(height,width,row,column)

            inputKernel = np.array([\
            [bwArray[ikc[0]],bwArray[ikc[1]],bwArray[ikc[2]]],
            [bwArray[ikc[3]],bwArray[ikc[4]],bwArray[ikc[5]]],
            [bwArray[ikc[6]],bwArray[ikc[7]],bwArray[ikc[8]]]\
            ])

            resultArray[row,column] = kernel_operator(inputKernel,kernelMatrix)

    return resultArray
