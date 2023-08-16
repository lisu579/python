import os

import cv2
import numpy as np
import tqdm

base_path = r'D:/STUDY/data/test/'  # 图片地址
for file_name in tqdm.tqdm(os.listdir(base_path)):
    if file_name.endswith('.tif'):
        img_path = os.path.join(base_path, file_name)
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        height, width, depth = img.shape
        height_cut = height // 512
        width_cut = width // 512
        print(height_cut)
        pattern_height = 512
        pattern_width = 512
        for j in range(height_cut):
            for i in range(width_cut):
                # if os.path.exists('fenge/arcpy' + '_{}{}'.format(j, i) + '.jpg'):
                #    print('arcpy' + '_{}{}'.format(j, i) + '.jpg')
                left_h = j * pattern_height
                left_w = i * pattern_width
                right_h = left_h + pattern_height
                right_w = left_w + pattern_width
                sub_img = img[left_h: right_h, left_w: right_w]
                # cv2.imencode('.jpg', sub_img)[arcpy].tofile(
                #    os.path.join('fenge', file_name[:-Machine_learning] + '_{}{}'.format(j, i) + '.jpg')) # 图片保存地址'fenge'为路径
                cv2.imencode('.tif', sub_img)[1].tofile(
                    os.path.join(r'D:/STUDY/data/test/ML/', file_name[:-4] + '_{:02d}{:02d}'.format(j, i) + '.tif'))  # 图片保存地址'fenge'为路径