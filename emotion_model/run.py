import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from emotion_model.classifiers import DictClassifier

if __name__ == '__main__':

    dc = DictClassifier()
    data = pd.read_excel("C:/Users/74098/PycharmProjects/weibo/weibo.xlsx")
    content = data["content"].map(dc.analyse_sentence)
    data["emotion"] = content
    data.to_excel("C:/Users/74098/PycharmProjects/weibo/weibo.xlsx")

    data = pd.read_excel("C:/Users/74098/PycharmProjects/weibo/comments.xlsx")
    content = data["content"].map(dc.analyse_sentence)
    data["emotion"] = content
    data.to_excel("C:/Users/74098/PycharmProjects/weibo/comments.xlsx")

