import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# train_test_split 划分训练集 测试集
# cross_val_score 交叉验证调节某个参数
# GridSearchCV 超参调节 调节多个参数
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
# roc_auc_score分数返回roc曲线下的面积
from sklearn.metrics import roc_auc_score, auc, roc_curve, f1_score, recall_score, precision_score, r2_score

data = pd.read_csv(r'D:\STUDY\data\test\moso.csv')
# print(data.head())

# 查看1和0的数量
# print(data.flag.value_counts())

# 把标记赋值给y
y = data.AGB
# print(y)
# 去掉标签列flag 赋值给x
x = data.drop('AGB',axis=1)
# print(x)
# y为标签 x为数据
# test_size表示测试集数据所占比例，random_state表示若要重复试验保证每次随机的实验结果是一样的
xtrain, xtest, ytrain, ytest = train_test_split(x, y,test_size=0.25, random_state=34 )

# RandomForestClassifier参数
# n_estimators 森林中树的数量，即基评估器的数量
# max_depth= 树的最大深度 默认为none 这样建树时，会使每一个叶节点只有一个类别，或是达到min_samples_split。
# min_samples_split:根据属性划分节点时，每个划分最少的样本数
# min_samples_leaf:叶子节点最少的样本数。
# criterion = 使用信息熵entropy或者基尼系数gini.默认是基尼系数
rfc = RandomForestRegressor(n_estimators=220,min_samples_leaf=10,min_samples_split=30,max_depth=8)#,random_state=10,
                            #,criterion='gini')class_weight=None)
rfc.fit(xtrain,ytrain)

# 导入测试集 rfc的接口score计算的是模型准确率accuracy
result = rfc.score(xtest,ytest)
print(result)

# 查看所有的决策树
# print(rfc.estimators_)

# 查看结果的类别
# print(rfc.classes_)
# 查看类别数量
# print(rfc.n_classes_)

# 查看预测结果标签值
# print(rfc.predict(xtest))

# 标签是1的可能性 出来的结果左边的标签值为0的概率 右边是标签值为1的概率
# print(rfc.predict_proba(xtest)[:,:])
# 只取标签为1的概率
# print(rfc.predict_proba(xtest)[:,arcpy])

# roc分数的计算
# sc = roc_auc_score(ytest,rfc.predict_proba(xtest)[:,arcpy])
# print(sc)

# 各个feature的重要性
print(rfc.feature_importances_)

#sklearn.model_selection.cross_val_score(estimator= ,X= , y= ,scoring= ,cv= ,n_jobs=, verbose= )
# estimator:估计方法对象(分类器)
# X: 数据特征(Features)
# y: 数据标签
# soring:调用方法（包括accuracy和mean_squared_error等等）
# cv: 几折交叉验证

r2 = r2_score(ytest, rfc.predict(xtest))
print(r2)
'''
# 结果统计 计算P,R,F1,accuracy
p = precision_score(list(ytest),rfc.predict(xtest))#,average='weighted')
r = recall_score(list(ytest),rfc.predict(xtest))#,average='weighted')
f1 = f1_score(list(ytest),rfc.predict(xtest))#,average='weighted')

print(p)    # 0.9038104235553457
print(r)    # 0.903448275862069
print(f1)   # 0.9034574607673332
'''




#  调整参数

# 查看训练集
# print(xtrain.shape)

# 调整森林中树的数量

param_test1 = {'n_estimators': range(20,500,10)}
# estimator输入分类器（分类器的参数）
# param_grid= 需要调参的超参名
# scoring = 每次评估使用的分数
# cv = 每次进行几折交叉验证
gsearch1 = GridSearchCV(estimator=RandomForestRegressor(min_samples_split=50,
                                                          min_samples_leaf=20,
                                                          max_depth=8,random_state=10),
                         param_grid=param_test1,
                         scoring='roc_auc')#,
                         #cv=correlation_slope_analysis)
gsearch1.fit(xtrain,ytrain)
# # 输出最好的参数和最好的分数
print(gsearch1.best_params_,gsearch1.best_score_)
# 输出结果 {'n_estimators': 220} 0.8620994691397194

# 调整最小样本数 和 最小叶节点的样本数
param_test2 = {'min_samples_split':range(20,200,10),'min_samples_leaf':range(10,200,10)}
gsearch2 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=220,
                                                         max_depth=8,random_state=10),
                        param_grid=param_test2,
                        scoring='roc_auc',
                        cv=3)
gsearch2.fit(xtrain,ytrain)
# 输出最好的参数和最好的分数
print(gsearch2.best_params_,gsearch2.best_score_)
# 输出结果{'min_samples_leaf': 10, 'min_samples_split': 30} 0.8675084144386757


# 调整最大深度
param_test3 = {'max_depth':range(2, 50, 2)}
gsearch3 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=220,
                                                         min_samples_leaf = 10,
                                                         min_samples_split = 30,
                                                         random_state=10),
                        param_grid=param_test3,
                        scoring='roc_auc',
                        cv=3)
gsearch3.fit(xtrain, ytrain)
# 输出最好的参数和最好的分数
print(gsearch3.best_params_, gsearch3.best_score_)
# 输出结果{'max_depth': 8} 0.8675084144386757

scor = roc_auc_score(ytest, gsearch3.best_estimator_.predict_proba(xtest)[:, 1])
print(scor)
# 0.964570943075616

print(gsearch3.best_estimator_)

# 调整分类方法 和样本平衡
# param_test4 = {'criterion':['gini','entropy'], 'class_weight':[None,'balanced']}
# gsearch4 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=220,
#                                                          min_samples_leaf=10,
#                                                          min_samples_split=30,
#                                                          max_depth=8,
#                                                          random_state=10),
#                         param_grid=param_test4,
#                         scoring='roc_auc',
#                         cv=correlation_slope_analysis)
# gsearch4.fit(xtrain,ytrain)
# print(gsearch4.best_params_, gsearch4.best_score_)
# {'class_weight': None, 'criterion': 'entropy'} 0.8722979957299399

# scor = roc_auc_score(ytest, gsearch4.best_estimator_.predict_proba(xtest)[:, arcpy])
# print(scor)
# 0.9615972812234495
