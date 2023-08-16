import os
import random
import shutil

def moveFile(train_img_Dir, train_mask_Dir):
        img_pathDir = os.listdir(train_img_Dir)                    # 提取图片的原始路径
        filenumber = len(img_pathDir)
        # 自定义test的数据比例
        test_rate = 0.2                                            # 如0.modis_preprocess，就是20%的意思
        test_picknumber = int(filenumber*test_rate)                # 按照test_rate比例从文件夹中取一定数量图片
               # 选取移动到test中的样本
        sample1 = random.sample(img_pathDir, test_picknumber)      # 随机选取picknumber数量的样本图片
        print(sample1)
        for i in range(0, len(sample1)):
            sample1[i] = sample1[i][:-4]                           # 去掉图片的拓展名，移动标注时需要这个列表
        for name in sample1:
            src_img_name1 = train_img_Dir + name
            dst_img_name1 = test_img_Dir + name
            shutil.move(src_img_name1 + '.tif', dst_img_name1 + '.tif')     # 加上图片的拓展名，移动图片
            src_mask_name1 = train_mask_Dir + name
            dst_mask_name1 = test_mask_Dir + name
            shutil.move(src_mask_name1 + '.tif', dst_mask_name1 + '.tif')   # 加上标注文件的拓展名，移动标注文件

        return

if __name__ == '__main__':
    # train 从train中移动
    train_img_Dir = r'D:/STUDY/data/test/ML/4/train/'
    train_mask_Dir = r'D:/STUDY/data/test/ML/4/validation/'
    # test路径：图片和标注目录
    test_img_Dir = r'D:/STUDY/data/test/ML/4/train1/'
    test_mask_Dir = r'D:/STUDY/data/test/ML/4/validation1/'

    # 运行划分数据集函数
    moveFile(train_img_Dir, train_mask_Dir)

