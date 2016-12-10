# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from math import pow,sqrt
import numpy as np
import kernel
import mainops

def gaussianBlur(bwArray):
    height = bwArray.shape[0]
    width = bwArray.shape[1]

    gaussianBlurKernel = np.array([
    [1,2,1],[2,4,2],[1,2,1]
    ])

    blurryArray = kernel.kernel_scan(bwArray,gaussianBlurKernel)

    return blurryArray

def boxBlur(bwArray):
    height = bwArray.shape[0]
    width = bwArray.shape[1]

    boxBlurKernel = np.array([
    [1,1,1],[1,1,1],[1,1,1]
    ])

    blurryArray = kernel.kernel_scan(bwArray,boxBlurKernel)

    return blurryArray
