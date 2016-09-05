# *-* coding: utf-8 -*-

import numpy as np

def kernel_operator(inputop, kernelop):
    opbuffer = np.zeros((kernelop.shape[0],kernelop.shape[1]))

    opbuffer = np.multiply(inputop,kernelop)
    pixel = np.sum(opbuffer)
    #print pixel

    return pixel
