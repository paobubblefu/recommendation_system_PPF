
# -*- coding: utf-8 -*-
# 使用LR进行MNIST手写数字分类
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# 加载数据
digits = load_digits()
data = digits.data
# 可视化
# print(data.shape)
# 查看第一幅图像
# print(digits.images[6])
# 第一幅图像代表的数字含义
# print(digits.target[6])
# 将第一幅图像显示出来
plt.gray()
plt.title('Handwritten Digits')
plt.imshow(digits.images[6])
# plt.show()

train_x, test_x, train_y, test_y = train_test_split(data, digits.target, test_size=0.25, random_state=33)

# 采用Z-Score规范化
ss = preprocessing.StandardScaler()
train_ss_x = ss.fit_transform(train_x)
test_ss_x = ss.transform(test_x)

# 创建LR分类器
lr = LogisticRegression(solver='lbfgs',multi_class='auto')
lr.fit(train_ss_x, train_y)
predict_y=lr.predict(test_ss_x)
print('LR准确率: %0.4lf' % accuracy_score(predict_y, test_y))

# -*- coding: utf-8 -*-
# Action1: 针对mnist数据集进行分类，采用CART决策树
from sklearn import tree
cart = tree.DecisionTreeClassifier(random_state=0,splitter='best',criterion='gini')

#训练集使用上个cell的数据
cart.fit(train_ss_x, train_y)
prediction = cart.predict(test_ss_x)
print('TREE准确率: %0.4lf' % accuracy_score(prediction, test_y))