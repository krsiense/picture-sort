# 读取文件夹下的图片，打乱patch，源地址生成“原名称+mixed”的图片

import os
from PIL import Image
import random
'''
用于读取本地文件夹下所有图片，分成64块，并保存生成的新图片
'''


def split_image(file_path):
    img = Image.open(file_path)
    w, h = img.size
    #print(w,h)
    new_img_list = []
    for i in range(8):
        for j in range(8):
            x = i * w / 8
            y = j * h / 8
            crop_img = img.crop((x, y, x + w / 8, y + h / 8))
            new_img_list.append(crop_img)
    random.shuffle(new_img_list)
    new_img = Image.new('RGB', (w, h))
    count = 0
    for i in range(8):
        for j in range(8):
            new_img.paste(new_img_list[count],  (int(j*w/8), int(i*h/8)))
            count += 1
    return new_img

if __name__ == '__main__':
    dir_path = r"D:\NewDesktop\puzzle\code0428"#"/path/to/images/"
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            file_path = os.path.join(dir_path, file_name)
            new_img = split_image(file_path)
            new_file_name = file_name.split(".")[0] + "mixed" + "." + file_name.split(".")[1]
            new_file_path = os.path.join(dir_path, new_file_name)
            new_img.save(new_file_path)