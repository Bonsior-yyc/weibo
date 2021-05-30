import pandas as pd
import os
from sklearn.model_selection import train_test_split
if not os.path.exists('weibo/data'):
    os.mkdir('weibo/data')


data = pd.read_excel('D:/vscodeWorkspace/rumor/weibo_new.xlsx')

content = []
label = []

for row in data.iterrows():
    content.append(row[1].content)
    label.append(row[1].label)

train_x, test_x, train_y, test_y = train_test_split(content, label, test_size=0.1)

with open('weibo/data/train.txt', 'w+') as f:
    for index in range(len(train_x)):
        f.write(train_x[index].replace('\n', '') + "\t" + str(train_y[index]) + '\n')

with open('weibo/data/test.txt', 'w+') as f:
    for index in range(len(test_x)):
        f.write(test_x[index].replace('\n', '') + "\t" + str(test_y[index]) + '\n')

with open('weibo/data/dev.txt', 'w+') as f:
    for index in range(len(test_x)):
        f.write(test_x[index].replace('\n', '') + "\t" + str(test_y[index]) + '\n')

with open('weibo/data/class.txt', 'w+') as f:
    f.write('非谣言\n谣言')
