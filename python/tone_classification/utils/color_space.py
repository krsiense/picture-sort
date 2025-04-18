from colormath.color_objects import sRGBColor, HSVColor
from colormath.color_conversions import convert_color


# 输入rgb范围是[0, 255]。如果输入是[0, 1]则需要将is_upscaled设为false
# 返回的hsv范围是：h=[0, 360], s=[0, 1], v=[0, 1]
def rgb2hsv(r, g, b):
    rgb = sRGBColor(r, g, b, is_upscaled=True)
    hsv = convert_color(rgb, HSVColor)
    h, s, v = hsv.get_value_tuple()
    return h, s, v


# 输入rgb的list
def rgb2hsv_list(rgblist):
    hsvlist = []
    for i in range(len(rgblist)):
        r,g,b = rgblist[i]
        rgb = sRGBColor(r, g, b, is_upscaled=True)
        h,s,v = convert_color(rgb, HSVColor).get_value_tuple()
        hsvlist.append([h, s, v])
    return hsvlist


if __name__ == '__main__':
    in_r, in_g, in_b = 0, 15, 100
    out_h, out_s, out_v = rgb2hsv(in_r, in_g, in_b)
    print(out_h, out_s, out_v)

