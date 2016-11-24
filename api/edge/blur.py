# *-* coding: utf-8 -*-

from mpi4py import MPI as mpi
from math import pow,sqrt
import numpy as np
import Image
import kernel
import mainops

def gaussianBlur(bwArray)
    gaussianBlurKernel = np.zeros((3,3))

    height = bwArray.shape[0]
    width = bwArray.shape[1]

    gaussianBlurKernel = np.array([
    [0,1,0],[-2,0,2],[-1,0,1]
    ])
