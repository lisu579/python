import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier

#Step1 读取数据+标签与数据分类
FilePath = r"D:\STUDY\data\test\feature.csv"
data1 = pd.read_csv(FilePath)
label = data1["biomass"]
feature = data1.drop(["biomass"], axis=1)
#填充缺失值
feature["arvi"].fillna(feature["arvi"].mean(), inplace=True)
feature.fillna('UNKNOWN', inplace=True)

#Step2 定义extra-tree特征筛选方法
def Extra_tree():
    Extra_model = ExtraTreesClassifier(random_state = 1)
    Extra_model.fit(feature, label)
    print(Extra_model.feature_importances_)

Extra_tree()