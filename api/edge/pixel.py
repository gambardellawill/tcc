# *-* coding: utf-8 -*-

import numpy as np

def brightness(bwArray,value):
    height = bwArray.shape[0]
    width = bwArray.shape[1]

    brightnessArray = np.ones((height,width)) * value

    resultArray = np.add(brightnessArray,bwArray)

    return resultArray

def contrast(bwArray,value):
    height = bwArray.shape[0]
    width = bwArray.shape[1]

    contrastArray = np.ones((height,width)) * (value + 0.5)
    resultArray = np.multiply(np.add(bwArray, -0.5*np.ones((height,width))), contrastArray)

    return resultArray
