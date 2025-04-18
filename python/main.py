from flask import Flask, jsonify,request
from flask_cors import CORS
from get_time.infer import base_work
from draw_img.get_blocks import draw_pic100,draw_pic64
from tone_classification.main_get_pallete import start_work
import json
app = Flask(__name__)
CORS(app)  # 这会为所有的路由添加CORS支持

data_path="../public/data/data.json"


import os

def has_same_named_folder(folder_path, folder_name):
    
    # 获取文件夹中的所有文件和文件夹列表
    contents = os.listdir(folder_path)

    # 检查是否有相同名称的文件夹
    for content in contents:
        # 使用 os.path.isdir() 检查路径是否为文件夹
        if os.path.isdir(os.path.join(folder_path, content)) and content == folder_name:
            return True

    return False

# 要检查的文件夹路径和文件夹名称
folder_path = '../public/results/'


@app.route('/save_img', methods=['POST'])
#上传图片，一次可多张
def save_image():
    # data = request.form  # 获取非文件数据
    # file = request.files  # 获取文件数据
    # # print("非文件数据：", data)
    # print("文件数据：", file['files[]'])

    # return jsonify({'message': 'Received data successfully'})


    # print(request.files)
    
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'})

    lastfile_path=[]
    files = request.files.getlist('files[]')
    for file in files:

        if file.filename == '':
            continue
    # 这里可以将文件保存到服务器的指定位置
        file.save('../public/images/' + file.filename)
        lastfile_path.append('/images/'+file.filename)
        print(lastfile_path)
        data_dict=base_work(file.filename)
        draw_pic64(file.filename)
        draw_pic100(file.filename)
        print(data_dict)

        try:
            with open(data_path, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        # 将新数据合并到现有数据中
        existing_data.update(data_dict)
        existing_data=sorted(existing_data.items(),key=lambda x:x[1]['time'],reverse=True)

        existing_data=dict(existing_data)
        # 将更新后的数据写入 JSON 文件
        with open(data_path, 'w') as file:
            json.dump(existing_data, file, indent=4) 


    return jsonify({'message': lastfile_path})


@app.route('/get_color',methods=['POST'])

def get_color():
    print(1111)
    print(request.data.decode('utf-8'))
    dir_name=request.data.decode('utf-8')
    if has_same_named_folder(folder_path,dir_name):
        print("true")
    else:
        # print(dir_name)
        start_work(dir_name)
        
        # files="hello"
        print("false")
    return jsonify({'message':"over"})


if __name__ == "__main__":
    app.run(debug=True, port=9000)