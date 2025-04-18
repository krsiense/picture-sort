

import os.path
import json
import numpy as np
import time

import PIL.Image as Image
import shutil
from colorsys import rgb_to_hsv

# kmeans方法
from tone_classification.kmean.deal_before import pre_process
from tone_classification.kmean.get_info import get_rgb
from tone_classification.kmean.palette import k_means

# 颜色空间
import tone_classification.color_space as cs
# 色度熵
from tone_classification.hue_entropy.Get_Hue_Entropy.getHueProbFeatures import getHueProbFeatures

from tone_classification.utils.judge_file import get_filenames, split_single_filenames


def get_complementary_color(colors_rgb_list, method):
    colors_size = len(colors_rgb_list)
    main_clr = colors_rgb_list[0]
    comp_clr = [255 - main_clr[0], 255 - main_clr[1], 255 - main_clr[2]]
    np_comp_clr = np.array(comp_clr)

    comp_clr_index = 0  # 哪个是补色?
    # 计算与理论上的补色np_comp_clr最近的颜色作为补色;
    if method == 1:
        min_dist = 100000
        for i in range(1, colors_size):
            v1 = np.array(colors_rgb_list[i])
            dist = np.linalg.norm(np_comp_clr - v1)
            if min_dist > dist:
                min_dist = dist
                comp_clr_index = i
    else:
        # 计算与主色的hue值距离最远的颜色作为补色
        colors_hsv = cs.rgb2hsv_list(colors_rgb_list)
        mainclr_hue = colors_hsv[0][0]
        max_hue_dist = 0
        for i in range(1, colors_size):
            cur_hue = colors_hsv[i][0]
            hue_dist = abs(cur_hue - mainclr_hue)
            if hue_dist > 180:
                hue_dist = 360 - hue_dist
            if hue_dist > max_hue_dist:
                max_hue_dist = hue_dist
                comp_clr_index = i
    return comp_clr_index


# 明度九调，nine_tone[0]="低中高", nine_tone[1]="短中长"
def get_v_nine_tone(main_clr, comp_clr):
    nine_tone = []
    _, _, main_color_v = cs.rgb2hsv(main_clr[0], main_clr[1], main_clr[2])
    _, _, comp_color_v = cs.rgb2hsv(comp_clr[0], comp_clr[1], comp_clr[2])
    nine_tone.append(get_grade_by_3level(main_color_v))

    v_dist = abs(main_color_v - comp_color_v)
    nine_tone.append(get_grade_by_3level(v_dist))

    return nine_tone


# 根据val的值分为[0-0.33,0.33-0.66,0.66-1]三个等级，分别表示0,1,2
def get_grade_by_3level(val):
    if val < 0.33:
        return 0
    elif val < 0.66:
        return 1
    else:
        return 2


# def get_features_from_image(input_pic, output_dir, filename):
#     image = Image.open(input_pic).convert('RGB')
#     image = image.resize((512, 512))
#     image.save(os.path.join(output_dir, filename))
#
#     color_features = {}
#     # colors_rgb表示返回的5种颜色的RGB数值, color_cluster表示对应的5种颜色的占比
#     colors_rgb, color_cluster = get_palette_from_img_by_kmeans(image, 5)
#     color_features['five_colors_rgb'] = colors_rgb
#     color_features['five_colors_area_percent'] = color_cluster
#
#     return color_features


# 获取图像特征属性
# def get_features_from_image(input_pic, output_dir, filename):
def get_features_from_image(input_pic):  # input_pic：输入需要获取特征属性的图片
    image = Image.open(input_pic).convert('RGB')
    image = image.resize((512, 512))
    # image.save(os.path.join(output_dir, filename))

    color_features = {}
    # colors_rgb表示返回的5种颜色的RGB数值, color_cluster表示对应的5种颜色的占比
    colors_rgb, color_cluster = get_palette_from_img_by_kmeans(image, 5)
    color_features['five_colors_rgb'] = colors_rgb
    color_features['five_colors_area_percent'] = color_cluster.tolist()

    # 转为hsv
    colors_hsv = cs.rgb2hsv_list(colors_rgb)
    np_hsv = np.array(colors_hsv)

    # 占比最大的主色的饱和度和亮度等级
    main_color_sat, main_color_val = np_hsv[0, :][1], np_hsv[0, :][2]
    color_features['main_color_saturate'] = main_color_sat
    color_features['main_color_saturate_level'] = get_grade_by_3level(main_color_sat)
    color_features['main_color_value'] = main_color_val
    color_features['main_color_value_level'] = get_grade_by_3level(main_color_val)

    # 5色组的亮度和饱和度分布的方差越小，表明5种颜色的亮度和饱和度越均匀
    np_hsv_diff = np.zeros([4, 3], dtype=float)
    for i in range(4):
        np_hsv_diff[i, :] = np.abs(np_hsv[i, :] - np_hsv[i + 1, :])
    diff_std = np.std(np_hsv_diff, axis=0)
    s_diff = diff_std[1]
    v_diff = diff_std[2]
    color_features['five_colors_sat_diff'] = s_diff
    color_features['five_colors_val_diff'] = v_diff

    # 色度熵，反映5种颜色的和谐程度
    _, hue_entropy = getHueProbFeatures(colors_rgb)
    color_features['five_colors_hue_entropy'] = hue_entropy

    # 补色index, 色轮上的最大距离颜色,并计算主色补色面积比
    comp_clr_index = get_complementary_color(colors_rgb, 2)
    main_comp_area_ratio = color_cluster[0] / color_cluster[comp_clr_index]
    # 补色是五色组中的第几个?
    color_features['comp_color_index'] = comp_clr_index
    color_features['main_comp_area_ratio'] = main_comp_area_ratio

    # 基于主色补色的明度九调
    nine_tone = get_v_nine_tone(colors_rgb[0], colors_rgb[comp_clr_index])
    color_features['color_nine_tone'] = nine_tone

    return color_features


# palette是array格式. 如果是list, 需要先转换为array
def get_bigger_palette_to_show(palette):
    c = 50
    palette_size = len(palette)
    palette2 = np.ones((1 * c, palette_size * c, 3))
    for i in range(palette_size):
        palette2[:, i * c:i * c + c, :] = palette[i, :].reshape((1, 1, -1))
    return palette2


# 保存主色调调色板图
def save_palette(colors_rgb, save_path):
    # colors_rgb：主色调五色RGB值array，save_path：保存路径
    palette_img = get_bigger_palette_to_show(np.array(colors_rgb))
    pimg = Image.fromarray(palette_img.round().astype(np.uint8))
    pimg.save(save_path)


def get_palette_from_img_by_kmeans(img, k):
    img_lab, n_pixels, n_channels = pre_process(img)
    centers, cluster_count = k_means(img_lab, k, init_mean=True, sortby='C', max_iter=1000, black=False)
    # 将Lab转为rgb
    colors_rgb = get_rgb(centers, cluster_count, n_channels, k)
    cluster_count = cluster_count / n_pixels

    return colors_rgb, cluster_count


# 清空文件夹
def clear_folder(folder_path):
    # 删除文件夹及其内部的所有文件和子文件夹
    shutil.rmtree(folder_path)
    # 重新创建一个空文件夹
    os.mkdir(folder_path)


# 输出指定色系的图片（主色调其中一个RGB距离接近即可）|暂废弃
def find_similar_color_images(rgb_value, image_colors, input_dir, output_dir):
    similar_images = []
    for image_file, colors in image_colors.items():
        for color in colors[:5]:  # 取前五个主色调进行比较
            if color_distance(color, rgb_value) < 100:  # 假设色彩距离小于100表示接近（RGB）
                # if color_distance(color, rgb_value) < 0.5:  # 假设色彩距离小于0.5表示接近（HSV）
                similar_images.append(image_file)
                break
    # 将相似图像复制到指定文件夹
    for image_file in similar_images:
        shutil.copy(os.path.join(input_dir, image_file), output_dir)


# 读图版|核心处理流程，输入指定色系的RGB值，调用find_similar_color_images输出该色系图片|暂废弃
def search_color_system(input_rgb, output_dir):
    palette_path = "../public/images"
    palette_filenames, palette_paths = split_single_filenames(palette_path)
    main_tone_dict_rgb = {}
    main_tone_dict_hsv = {}
    for i, item in enumerate(palette_paths):
        image = Image.open(item)
        width, height = image.size
        main_tone_rgb = []
        main_tone_hsv = []
        block_width = width // 5  # 假设有五个色块
        for j in range(5):
            left = j * block_width
            upper = 0
            right = (j + 1) * block_width
            lower = height
            block = image.crop((left, upper, right, lower))
            main_tone_rgb.append(block.getpixel((block_width // 2, height // 2)))  # 获取中心像素的RGB值
            rgb_color = block.getpixel((block_width // 2, height // 2))
            main_tone_hsv.append(rgb_to_hsv(rgb_color[0] / 255, rgb_color[1] / 255, rgb_color[2] / 255))  # 获取中心像素的HSV值

        # 使用列表推导式创建字典，假设将 RGB 元组作为键，索引作为值
        main_tone_dict_rgb[f"{palette_filenames[i]}.jpg"] = main_tone_rgb
        main_tone_dict_hsv[f"{palette_filenames[i]}.jpg"] = main_tone_hsv
    print(main_tone_dict_rgb)
    # print(main_tone_dict_hsv)

    input_dir = "../public/images"
    input_hsv = rgb_to_hsv(input_rgb[0] / 255, input_rgb[1] / 255, input_rgb[2] / 255)
    find_similar_color_images(input_rgb, main_tone_dict_rgb, input_dir, output_dir)
    # find_similar_color_images(input_hsv, main_tone_dict_hsv, input_dir, output_dir)
    print("——处理完毕——\n")


# 计算RGB颜色距离
def color_distance(color1, color2):
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5


# 计算单张图主色调与指定RGB值之间的相似度
def count_similar_percent(refer_rgb, image_main_rgb, rgb_percent, color_threshold=100):
    # refer_rgb：选取的指定RGB，主色调跟它比，image_main_rgb：图片主色调RGB, rgb_percent：图片主色调占比，color_threshold：相似阈值
    similar_percent = 0
    for i, color in enumerate(image_main_rgb[:5]):
        if color_distance(color, refer_rgb) < color_threshold:
            similar_percent += rgb_percent[i]
    return similar_percent


# 读文件数据版|核心处理流程（RGB距离接近的主色调占20%及以上）
def judge_similar(input_rgb, output_json):
    similar_results = {}
    for i in output_json:
        file_color_features = output_json[i]
        colors_rgb = file_color_features["five_colors_rgb"]
        colors_percent = file_color_features["five_colors_area_percent"]

        similar_percent = count_similar_percent(input_rgb, colors_rgb, colors_percent, 100)
        similar_results[i] = similar_percent
    sorted_dict = dict(sorted(similar_results.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict


# 计算数字位数
def num_digits(n):
    n = abs(n)
    if n == 0:
        return 1
    count = 0
    while n > 0:
        n //= 10
        count += 1
    return count


# 输出结果
def print_results(similar_results, output_json, length,color):
    digit_len = num_digits(length)
    input_dir = f"../public/images"
    out_json={}
    # 将相似图像复制到指定文件夹  
    # 更正，只需要在指定文件夹输出一个json文件即可
    for index, item in enumerate(similar_results):
        similar_percent = similar_results[item]
        if similar_percent >= 0.2:
            # input_path = os.path.join(input_dir, f"{item}.jpg")
            # now_time = time.time()
            # print(now_time, item, similar_results[item])
            # output_path = os.path.join(output_dir, f"{str(index).zfill(digit_len)}-{item}.jpg")
            # print(input_path)
            # print(output_path)
            # shutil.copy(input_path, output_path)
            out_json.update({f"{item}":output_json[item]})
    with open('../public/results/'
                f'{color}/output_json.json', 'w') as json_file:
                        json.dump(out_json, json_file)
    return 0


def start_work(in_path):
    origin_filenames, origin_inputs = get_filenames()
    compress_path = "../public/compress"
    palette_path = "../public/palette"
    results_path = "../public/results"
    if not os.path.exists(compress_path):
        os.mkdir(compress_path)
    if not os.path.exists(palette_path):
        os.mkdir(palette_path)
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    compress_origin, _ = split_single_filenames(compress_path)
    palette_origin, _ = split_single_filenames(palette_path)

    while True:
        compress_origin, _ = split_single_filenames(compress_path)
        palette_origin, _ = split_single_filenames(palette_path)

        # input_rgb = input("请输入一个RGB值（以西文逗号为分隔符）：")
        input_rgb=in_path
        if input_rgb.lower() == "exit":
            break
        split_rgb = [int(num) for num in input_rgb.split(",")]
        if len(split_rgb) == 3:
            wrong_flag = False
            for item in split_rgb:
                if item < 0 or item > 255:
                    wrong_flag = True
            if wrong_flag:
                print("输入不合法！")
            else:
                print(f"——开始寻找主色调接近{input_rgb}的图片——\n")

                output_dir = f"../public/results\\{input_rgb}"
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)
                else:
                    clear_folder(output_dir)

                if len(compress_origin) < len(origin_inputs) or len(palette_origin) < len(origin_inputs):
                    output_json = {}
                    for i in range(len(origin_inputs)):
                        print(f"——开始处理第{str(i + 1)}张图片——")
                        # 从图像提取颜色特征
                        # file_color_features = get_features_from_image(origin_inputs[i], compress_path,
                        #                                               f"{origin_filenames[i]}.jpg")
                        file_color_features = get_features_from_image(origin_inputs[i])
                        # 颜色特征打印
                        print("5组主色调的RGB值：", file_color_features['five_colors_rgb'])
                        print("5组主色调在图像中的占比：", file_color_features['five_colors_area_percent'], "\n")

                        colors_rgb = file_color_features['five_colors_rgb']
                        save_palette(colors_rgb, os.path.join(palette_path, f"{origin_filenames[i]}.jpg"))
                        colors_percent = file_color_features['five_colors_area_percent']

                        output_json[origin_filenames[i]] = file_color_features

                    # 将字典数据写入到 JSON 文件中
                    with open('../public/data/'
                              'output_json.json', 'w') as json_file:
                        json.dump(output_json, json_file)
                    
                    similar_results = judge_similar(split_rgb, output_json)
                    length = len(output_json)
                    print_results(similar_results, output_json, length,input_rgb)
                    
                    if i == len(origin_inputs)-1:
                        print("——处理完毕——\n")
                        break
                else:
                    # 从 JSON 文件中读取数据
                    with open('../public/data/'
                              'output_json.json', 'r') as json_file:
                        output_json = json.load(json_file)
                    similar_results = judge_similar(split_rgb, output_json)
                    length = len(output_json)
                    print_results(similar_results, output_json, length,input_rgb)
                    # search_color_system(split_rgb, output_dir)
                    print("——处理完毕——\n")
                    break
        else:
            print("输入不合法！")
