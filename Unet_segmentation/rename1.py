import os
import sys

filePath="D:\STUDY\data\road\train\output"
files=os.listdir(filePath)

def rename(filePath):

    condition = ('.tif')

     for fileName in files:
         if fileName != sys.argv[0]:
            if fileName.endswith(condition):
                os.rename(os.path.join(root, fileName), os.path.join(root, fileName.split('.')[0] + '_' +
                                                                         mark + '.' + fileName.split('.')[-1]))
                print(fileName, '已经重命名成功了，乖乖，新名字是：', fileName.split('.')[0] + '_' + mark + '.'
                          + fileName.split('.')[-1])



if __name__ == '__main__':
    filePath = r'G:\村级裁剪'
    rename(filePath)
