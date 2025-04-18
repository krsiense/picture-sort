# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:26:11 2020

@author: lenovo
"""

import math
import numpy as np
import mpmath


def circ_vmpdf(alpha, thetahat, kappa):
    
    alpha = alpha;
    
    C = 1/(2*math.pi*mpmath.besseli(0,kappa));
    aas = [];
    
    for i in range(len(alpha)):
        a = alpha[i]-thetahat
        aa = math.exp(kappa*math.cos(a));
        aas.append(aa);
    aas = np.array(aas);
    b = aas;
    #b = float( math.exp(kappa*aas));
    p = C * b;
    return p ;