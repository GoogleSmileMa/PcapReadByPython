import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import Imputer
import csv
import datetime
a = csv.reader(open('Tor_TimeBasedFeatures_10s_Layer2_10.csv', 'r'))
data = []
label = []
for row in a:
    data.append(row[:-1])
    label.append(int(row[-1]))
dataset = np.array(data, dtype=float)
# print(len(dataset))
# print(len(label))
dataset = Imputer().fit_transform(dataset)
x_train, x_test, y_train, y_test = train_test_split(dataset, label, test_size=1/3., random_state=8)  # 分割训练集和测试集
print(x_train.shape)
print(x_test.shape)
estimators = {}
estimators['tree'] = tree.DecisionTreeClassifier(criterion='gini', random_state=8)  # 决策树
estimators['forest'] = RandomForestClassifier(n_estimators=20, criterion='gini', bootstrap=True, n_jobs=2, random_state=8)  # 随机森林
# estimators['SVM'] = SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')  # 支持向量机
estimators['KNN'] = KNeighborsClassifier(3)  # K近邻
estimators['Bayes'] = MultinomialNB(alpha=0.0001)  # 朴素贝叶斯
estimators['MLP'] = MLPClassifier(solver='lbfgs', alpha=1e-4, random_state=1)  # 神经网络，hidden_layer_sizes=(5, 2),
for k in estimators.keys():
    start_time = datetime.datetime.now()
    print('----%s----' % k)
    estimators[k] = estimators[k].fit(x_train, y_train)
    pred = estimators[k].predict(x_test)
    print(pred[:10])
    print("%s Score: %0.4f" % (k, estimators[k].score(x_test, y_test)))
    scores = cross_val_score(estimators[k], x_train, y_train, scoring='accuracy', cv=10)
    print("%s Cross Avg. Score: %0.4f (+/- %0.4f)" % (k, scores.mean(), scores.std() * 2))
    end_time = datetime.datetime.now()
    time_spend = end_time - start_time
    print("%s Time: %0.2f" % (k, time_spend.total_seconds()))
