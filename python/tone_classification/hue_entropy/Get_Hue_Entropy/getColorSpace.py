# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:51:42 2020

@author: lenovo
"""
import math
import numpy as np

from scipy import interpolate

from tone_classification.hue_entropy.Get_Hue_Entropy import rgbhsv


def getColorSpaces(rgb):

    hsvs = [];
    r,g,b = rgb[0,0] ,rgb[1,0] , rgb[2,0];
    hsv = rgbhsv.rgb2hsv(r,g,b);
    hsv = np.array(hsv);
    hsvs.append(hsv);
    r,g,b = rgb[0,1] ,rgb[1,1] , rgb[2,1];
    hsv = rgbhsv.rgb2hsv(r,g,b);
    hsv = np.array(hsv);
    hsvs.append(hsv);
    r,g,b = rgb[0,2] ,rgb[1,2] , rgb[2,2];
    hsv = rgbhsv.rgb2hsv(r,g,b);
    hsv = np.array(hsv);
    hsvs.append(hsv);
    r,g,b = rgb[0,3] ,rgb[1,3] , rgb[2,3];
    hsv = rgbhsv.rgb2hsv(r,g,b);
    hsv = np.array(hsv);
    hsvs.append(hsv);
    r,g,b = rgb[0,4] ,rgb[1,4] , rgb[2,4];
    hsv = rgbhsv.rgb2hsv(r,g,b);
    hsv = np.array(hsv);
    hsvs.append(hsv);

    hsvs = np.array(hsvs)

    hsvs = hsvs;

    return hsvs;
    