# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from math import pow,sqrt
import numpy as np
import kernel
import mainops

def sharpen(bwArray):
    height = bwArray.shape[0]
    width = bwArray.shape[1]

    sharpeningKernel = np.array([
    [0,-1,0],[-1,5,-1],[0,-1,0]
    ])

    sharpenArray = kernel.kernel_scan(bwArray,sharpeningKernel)

    return sharpenArray
