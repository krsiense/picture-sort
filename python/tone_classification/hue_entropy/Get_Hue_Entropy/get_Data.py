# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:14:50 2020
@author: lenovo
"""

import os
import scipy.io
import numpy as np

def get_KulerX():
    path = os.getcwd()+"/tone_classification/"
    mat_file= os.path.join(path,'hue_entropy/data/kulerX.mat')
    KulerX = scipy.io.loadmat(mat_file);
    x = KulerX['x'];
    return x;
 
def get_HueProb():
    path = os.getcwd()+"/tone_classification/"
    mat_file= os.path.join(path,'hue_entropy/data/hueProbsRGB.mat')
    KulerX = scipy.io.loadmat(mat_file);
    x = KulerX['hueProbs']
    y = x[0,0]['hueProb']
    
    return y;

def get_HueJoint():
    path = os.getcwd()+"/tone_classification/"
    mat_file= os.path.join(path,'hue_entropy/data/hueProbsRGB.mat')
    KulerX = scipy.io.loadmat(mat_file);
    x = KulerX['hueProbs']
    y = x[0,0]['hueJoint']
    #print(np.array(y))
    #print(y.shape)
    return y;

def get_HueAdjacency():
    path = os.getcwd()+"/tone_classification/"
    mat_file= os.path.join(path,'hue_entropy/data/hueProbsRGB.mat')
    KulerX = scipy.io.loadmat(mat_file)
    x = KulerX['hueProbs']
    y = x[0,0]['hueAdjacency']
    
    return y

def get_HueSaturation():
    path = os.getcwd()+"/tone_classification/"
    mat_file= os.path.join(path,'hue_entropy/data/hueProbsRGB.mat')
    KulerX = scipy.io.loadmat(mat_file)
    x = KulerX['hueProbs']
    y = x[0,0]['hueSaturation']
    
    return y