import numpy as np
from Get_Hue_Entropy.getColorSpace import getColorSpaces
from Get_Hue_Entropy.getHueProbFeatures import getHueProbFeatures


def test_hue_entropy():
    colors = [[220,37,10],[220,167,30],[20,167,20],[20,127,180],[120,100,250]];
    hueFeatures, entropy = getHueProbFeatures(colors)
    print("色相熵为：{}".format(entropy))



if __name__ == '__main__':
    test_hue_entropy()


