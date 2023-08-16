import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

#Step1 读取数据+标签与数据分类        # 这里应该要把生物量ABG也放进去，参考原文的csv文件
FilePath = r"D:\STUDY\data\test\S1_AGB_19Jun3.csv"
data1 = pd.read_csv(FilePath)
label = data1["AGB"]
feature = data1.drop(["AGB"], axis=1)
'''#填充缺失值
feature["arvi"].fillna(feature["arvi"].mean(), inplace=True)
feature.fillna('UNKNOWN', inplace=True)'''

#Step2 定义线性SVC和Logistic回归的迭代模型
def SVC_RFE():
    svc = SVC(kernel = "linear", C=1)
    rfe = RFE(estimator=svc, n_features_to_select=10, step=1)
    rfe.fit(feature, label)
    print(rfe.n_features_)  # 打印最优特征变量数
    print(rfe.support_)  # 打印选择的最优特征变量
    print(rfe.ranking_)  # 特征排序

def LR_RFE():
    LR = LogisticRegression()
    rfe = RFE(estimator=LR, n_features_to_select=10, step=1)
    rfe.fit(feature, label)
    print(rfe.n_features_)  # 打印最优特征变量数
    print(rfe.support_)  # 打印选择的最优特征变量
    print(rfe.ranking_)  # 特征排序

SVC_RFE()
LR_RFE()