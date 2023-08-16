import pandas as pd;
import os
from tkinter import filedialog,Tk

root = Tk()    # 创建一个Tkinter.Tk()实例
files_path = filedialog.askdirectory(initialdir='D:\\',title = "请选择要批处理的文件夹")                      # 视频所在文件夹的路径位置,默认C盘
root.destroy()  # 将Tkinter.Tk()实例销毁

#找到所有文件名
files = os.listdir(files_path)

#创建一个新目录存放 csv 文件
csv_path = files_path + '/csv格式'
if  not os.path.exists(csv_path):  # 如果目录不存在就创建
    os.makedirs(csv_path)


#循环，批量把excel改成csv
for i in files:
    df = pd.read_excel(files_path + '/' + i)        # 打开文件
    (filename, extension) = os.path.splitext(i)     # 分割文件名和文件后缀（扩展名）
    output = csv_path + '/' +  filename + ".csv"    # 构造绝对路径
    print(output)
    df.to_csv(output,index=0,header=0)              # 不要索引,也不要把第一行当列名

print('ok')
