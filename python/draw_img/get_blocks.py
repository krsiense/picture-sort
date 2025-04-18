from PIL import Image, ImageDraw

def draw_pic64(name):
    # 源图像路径
    path="../public/images/"+name

    # 打开图像文件
    image = Image.open(path)

    # 获取图像的宽度和高度
    width, height = image.size

    # 计算每个小块的宽度和高度
    block_width = width // 8
    block_height = height // 8

    # 创建一个新的图像，以源图像作为背景
    result_image = image.copy()
    draw = ImageDraw.Draw(result_image)

    # 画水平线
    for y in range(1, 8):
        draw.line((0, y * block_height, width, y * block_height), fill="black",width=3)

    # 画垂直线
    for x in range(1, 8):
        draw.line((x * block_width, 0, x * block_width, height), fill="black",width=3)

    # 保存结果图像
    result_image.save(f"../public/images64/{name}")


def draw_pic100(name):
    # 源图像路径
    path="../public/images/"+name

    # 打开图像文件
    image = Image.open(path)

    # 获取图像的宽度和高度
    width, height = image.size

    # 计算每个小块的宽度和高度
    block_width = width // 10
    block_height = height // 10

    # 创建一个新的图像，以源图像作为背景
    result_image = image.copy()
    draw = ImageDraw.Draw(result_image)

    # 画水平线
    for y in range(1, 10):
        draw.line((0, y * block_height, width, y * block_height), fill="black",width=5)

    # 画垂直线
    for x in range(1, 10):
        draw.line((x * block_width, 0, x * block_width, height), fill="black",width=5)

    # 保存结果图像
    result_image.save(f"../public/images100/{name}")
