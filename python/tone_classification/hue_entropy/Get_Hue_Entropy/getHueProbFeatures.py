# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 20:32:18 2020

@author: lenovo
"""
import numpy as np
import math

# from Get_Hue_Entropy import get_Data, getBasicStats, circ_vmpdf
# from Get_Hue_Entropy.getColorSpaces import getColorSpaces
from tone_classification.hue_entropy.Get_Hue_Entropy import get_Data, getBasicStats, circ_vmpdf
from tone_classification.hue_entropy.Get_Hue_Entropy.getColorSpace import getColorSpaces


def getHueProbFeatures(colors):


    '''准备工作'''
    colors = np.array(colors)
    colors = np.transpose(colors)
    satValThresh = 0.2
    hsv = getColorSpaces(colors)
    hsv = hsv / 255;
    hsv = np.transpose(hsv)



    hues=[];

    hueJoint = get_Data.get_HueJoint();
    hueAdjacency = get_Data.get_HueAdjacency();
    hueProb = get_Data.get_HueProb();
    hsv = hsv;

    one = hsv[1:3,:]

    selectColors = (min(hsv[1:2,:])>=satValThresh);
    a = np.array([[359],[100],[100]]);
    repmat = np.tile(a,(1,5));
    #repmat = repmat.T

    hsv2=np.round(hsv*repmat)+1;
    
    visHues=hsv2[0,selectColors];
    hueJointList=[];
    for h1 in range(len(visHues)):
        for h2 in range(h1,len(visHues)):
            one_use = visHues[h2]-1;
            two_use = visHues[h1]-1;
            three = hueJoint[int(visHues[h2]-1),int(visHues[h1]-1)];
            hueJointList.append(hueJoint[int(visHues[h2]-1),int(visHues[h1]-1)]);
            #hueJointList = np.array([hueJointList,);

    hueAdjList=[];
    for h1 in range(0,(len(visHues)-1)):
        hueAdjList.append(hueAdjacency[int(visHues[h1]-1),int(visHues[h1+1]-1)]  );
        #hueAdjList=[hueAdjList ()];
    
    hues = [];
    hue = [];
    for h in range(len(visHues)):
        hue = hueProb[int(visHues[h]-1)];
        hues.append(hue);
        


    hueProbFeatures= getBasicStats.getBasicStats(hues, 1);
    hueJointProbFeatures= getBasicStats.getBasicStats_2(hueJointList, 1);
    hueAdjProbFeatures= getBasicStats.getBasicStats_2(hueAdjList, 1);
    
    alpha = np.linspace(0, 2*math.pi, 361);
    end = len(alpha);
    alpha = alpha[0:end-1]
    # print(alpha)
    pMix=0.001*np.ones(len(alpha))
    visHues = visHues / 360
    for j in range(len(visHues)):
        pMix = pMix + circ_vmpdf.circ_vmpdf(alpha, (visHues[j]) * 2 * math.pi, 2 * math.pi);
    pMix=pMix/sum(pMix);
    pMixs = [];
    for i in range(len(pMix)):
        pMixs.append(pMix[i]);
    pMixs = np.array(pMixs);

    sum1 = [];
    if len(visHues) != 0:
        for i in range(len(pMixs)):
            #这里可以作为一个检查点
            r = math.log(pMixs[i]);
            sum1.append(pMixs[i] * r);
        sum1 = np.array(sum1);
        entropy=float(-sum(sum1));
    else:
        entropy=5.9;


    hueFeatures1 = [];
    hueFeatures2 = [];
    hueFeatures3 = [];
    
    for i in range(len(hueProbFeatures)):
        hueFeatures1.append(hueProbFeatures[i]);

    hueFeatures1 = np.array(hueFeatures1);
    
    for i in range(len(hueJointProbFeatures)):
        hueFeatures2.append(hueJointProbFeatures[i]);
    hueFeatures2 = np.array(hueFeatures2);
    for i in range(len(hueAdjProbFeatures)):
        hueFeatures3.append(hueAdjProbFeatures[i]);
    hueFeatures3 = np.array(hueFeatures3);

    hueFeatures = [hueFeatures1,hueFeatures2,hueFeatures3];

    hueFeatures = np.array(hueFeatures);
    
    
    hueFeatures = hueFeatures.reshape(1,24);
    hueFeatures = hueFeatures[0];
    b = np.array(entropy);
    hueFeatures = np.insert(hueFeatures,24,values = entropy,axis = 0);
    
    return hueFeatures,entropy;