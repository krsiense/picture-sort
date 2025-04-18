# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:17:05 2020

@author: lenovo
"""

# matlab格式下rgb转hsv
def rgb2hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/df)*60;
        else:
            h = ((g-b)/df)*60 + 360 ;

    elif mx == g:
        h = (60 * ((b - r) / df) + 120);
    elif mx == b:
        h = (60 * ((r - g) / df) + 240);
    if mx == 0:
        s = 0
    else:
        s = df / mx
    v = mx
    # H = h / 2
    #最后检查这里。必须查看这里为什么和matlab差这么多
    H = h * 0.70835;
    S = s * 255.0
    V = v * 255.0
    return H,S,V


# def rgb2hsv(r, g, b):
#     r, g, b = r/255.0, g/255.0, b/255.0
#     mx = max(r, g, b)
#     mn = min(r, g, b)
#     m = mx-mn
#     if mx == mn:
#         h = 0
#     elif mx == r:
#         if g >= b:
#             h = ((g-b)/m)*60
#         else:
#             h = ((g-b)/m)*60 + 360
#     elif mx == g:
#         h = ((b-r)/m)*60 + 120
#     elif mx == b:
#         h = ((r-g)/m)*60 + 240
#     if mx == 0:
#         s = 0
#     else:
#         s = m/mx
#     v = mx
#     H = h/2;
#     S = s * 255.0
#     V = v * 255.0
#     return H,S,V;