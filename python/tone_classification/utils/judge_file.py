import os


def judge_image(filename):
    return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])


def split_single_filenames(input_dir):
    fileNames = []
    img_filenames = []
    for x in os.listdir(input_dir):
        if judge_image(x):
            fileName = os.path.splitext(x)[0]
            fileNames.append(fileName)
            img_filename = os.path.join(input_dir, x)
            img_filenames.append(img_filename)

    return fileNames, img_filenames


def get_filenames():
    dir_origin = "..\public\images"
    fileNames_origin, path_filenames_origin = split_single_filenames(dir_origin)
    return fileNames_origin, path_filenames_origin
