import os

class BatchRename():

    def rename(self):
        path = r"D:\STUDY\data\test\ML\4\train"
        filelist = os.listdir(path)
        total_num = len(filelist)
        #i = 0
        for filename in filelist:
            if filename.endswith('.tif'):
                src = os.path.join(os.path.abspath(path), filename)
                dst = os.path.join(os.path.abspath(path), filename.split('_')[-1] )
                try:
                    os.rename(src, dst)

                except:
                    continue
        print(filename, '已经重命名成功了，新名字是：', filename.split('_')[-1] )


if __name__ == '__main__':
    demo = BatchRename()
    demo.rename()

'''
def make_dataset(root):

    imgs=[]
    filelist = os.listdir(root)
    n = len(filelist)
    for filename in filelist:
        if filename.endswith('re.tif'):
            img=os.path.join(root,filename)
        if filename.endswith('15.tif'):
            mask=os.path.join(root,filename)
            imgs.append((img,mask))
    return imgs'''