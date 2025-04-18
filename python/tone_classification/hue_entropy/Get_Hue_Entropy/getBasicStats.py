# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 20:39:59 2020

@author: lenovo
"""
import numpy as np
import math

def getBasicStats(x,addLog):
    x = np.array(x);
    
    if len(x)>0:

        log_x = [];
        for i in range(len(x)):
            log_x.append(math.log(x[i]+0.000001));
        log_x = log_x;
        if len(x) == 1:
            features = np.array(
                [np.mean(x), np.nan, min(x)[0], max(x)[0], np.mean(log_x), np.nan, min(log_x),
                 max(log_x)]);
        else:

            features = np.array(
                [np.mean(x), np.std(x, ddof=1), min(x)[0], max(x)[0], np.mean(log_x), np.std(log_x, ddof=1), min(log_x),
                 max(log_x)]);
    else:
        features=np.zeros(8);
    
    #print("---------------")
    #print(features)
    features = np.array(features);
    features[np.isinf(features)]=0;
    features[np.isnan(features)]=0;
    
    return features;
    
def getBasicStats_2(x,addLog):
    x = np.array(x);
    
    if len(x)>0:
        #log_x=math.log(x+0.000001);
        log_x = [];
        for i in range(len(x)):
            log_x.append(math.log(x[i]+0.000001));
        if len(x) == 1:
            features = np.array(
                [np.mean(x), np.nan, min(x), max(x), np.mean(log_x), np.nan, min(log_x),
                 max(log_x)]);

        else:

            features = np.array(
                [np.mean(x), np.std(x, ddof=1), min(x), max(x), np.mean(log_x), np.std(log_x, ddof=1), min(log_x),
                 max(log_x)]);

    else:
        features=np.zeros(8);

    features = np.array(features);
    features[np.isinf(features)]=0.0;
    features[np.isnan(features)]=0.0;

    return features;
        