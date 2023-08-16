import os
import sys


def rename(filePath):
    """
    批量重命名指定路径下的'.dbf', '.prj', '.shp', '.shx'格式的文件，重命名格式：文件_文件夹名字，
    并删除'.sbn', '.sbx', '.xml'格式的文件
    :param filePath: 文件夹的路径
    :return:
    """
    # 文件筛选条件
    condition1 = ('.dbf', '.prj', '.shp', '.shx')
    condition2 = ('.sbn', '.sbx', '.xml')

    # os.walk 查找文件
    for root, dirs, files in os.walk(filePath):
        # 文件夹名字
        mark = root.split('\\')[-1]

        # for循环遍历文件名字
        for fileName in files:
            if fileName != sys.argv[0]:
                if fileName.endswith(condition1):
                    os.rename(os.path.join(root, fileName), os.path.join(root, fileName.split('.')[0] + '_' +
                                                                         mark + '.' + fileName.split('.')[-1]))
                    print(fileName, '已经重命名成功了，乖乖，新名字是：', fileName.split('.')[0] + '_' + mark + '.'
                          + fileName.split('.')[-1])
                if fileName.endswith(condition2):
                    delFileName = os.path.join(root, fileName)
                    os.remove(delFileName)
                    print(delFileName, '已经成功被移除。')


if __name__ == '__main__':
    filePath = r'G:\村级裁剪'
    rename(filePath)
