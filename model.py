import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from importlib import import_module

from language_model.train_eval import train, getOutput
from language_model.utils import build_dataset, build_iterator
from user_model.model import get_user_model
from emotion_model.model import get_emotion_model
from tensorflow import keras


def train_language(_train=False):
    dataset = 'C:/Users/74098/PycharmProjects/weibo/weibo'  # 数据集
    x = import_module('language_model.models.bert')
    config = x.Config(dataset)
    print(config.device)
    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True  # 保证每次结果一样

    print("Loading data...")
    train_data, dev_data, test_data = build_dataset(config)
    train_iter = build_iterator(train_data, config)
    dev_iter = build_iterator(dev_data, config)
    test_iter = build_iterator(test_data, config)

    # train
    model = x.Model(config).to(config.device)
    if _train:
        train(config, model, train_iter, dev_iter, test_iter)
    else:
        model.load_state_dict(torch.load(config.save_path))
    return model, test_iter, train_iter


def get_model():
    return keras.Sequential([
        keras.layers.Dense(32, input_shape=(3,), activation='relu'),
        keras.layers.Dense(64, activation='relu'),

        keras.layers.Dropout(0.25),

        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])


def get_user(tran_train_x, tran_test_x, train_y, _train=False):
    if _train:
        um = get_user_model()
        um.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        um.fit(tran_train_x, train_y, epochs=100)
        um.evaluate(tran_test_x, test_y)
        um.save("user_model_saved")
        return um
    else:
        return keras.models.load_model('user_model_saved')


def get_emotion(emo_train_x, emo_test_x, train_y, _train=False):
    if _train:
        em = get_emotion_model()
        em.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        em.fit(emo_train_x, train_y, epochs=100)
        em.evaluate(emo_test_x, test_y)
        em.save("emotion_model_saved")
        return em
    else:
        return keras.models.load_model('emotion_model_saved')


if __name__ == '__main__':
    import warnings
    from collections import Counter

    warnings.filterwarnings('ignore')

    trans_features = ["comment_number", "thumb_number", "repost_number", "is_certified", "follow_number", "fan_number",
                      "weibo_number", 'wis', "pti"]

    emotion_features = ["emotion", "emotion_mean", "emotion_std", "emotion_jc"]

    data = pd.read_excel("C:/Users/74098/PycharmProjects/weibo/weibo.xlsx")
    data = data.fillna('0')

    x, y = data[trans_features + emotion_features + ["content"]], data['rumor']

    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.1, random_state=5)

    print(len(train_x), len(test_x))

    with open('weibo/data/train.txt', 'w+') as f:
        for index, row in train_x.iterrows():
            f.write(row['content'].replace('\n', '') + "\t" + str(train_y[index]) + '\n')

    with open('weibo/data/test.txt', 'w+') as f:
        for index, row in test_x.iterrows():
            f.write(row['content'].replace('\n', '') + "\t" + str(test_y[index]) + '\n')

    with open('weibo/data/dev.txt', 'w+') as f:
        for index, row in test_x.iterrows():
            f.write(row.content.replace('\n', '') + "\t" + str(test_y[index]) + '\n')

    with open('weibo/data/class.txt', 'w+') as f:
        f.write('非谣言\n谣言')

    train_x = train_x.drop("content", axis=1).astype('float64')
    test_x = test_x.drop("content", axis=1).astype('float64')

    emo_train_x = train_x[emotion_features]
    emo_test_x = test_x[emotion_features]
    emo_scale = StandardScaler()
    emo_scale.fit(emo_train_x)
    emo_train_x = emo_scale.transform(emo_train_x)
    emo_test_x = emo_scale.transform(emo_test_x)

    tran_train_x = train_x[trans_features]
    tran_test_x = test_x[trans_features]
    tran_scale = StandardScaler()
    tran_scale.fit(tran_train_x)
    tran_train_x = tran_scale.transform(tran_train_x)
    tran_test_x = tran_scale.transform(tran_test_x)

    language_model, test_iter, train_iter = train_language()
    um = get_user(tran_train_x, tran_test_x, train_y)
    em = get_emotion(emo_train_x, emo_test_x, train_y)

    print(Counter((um.predict(tran_test_x[test_y == 0]) > 0.5).flatten()))
    print(Counter((um.predict(tran_test_x[test_y == 1]) > 0.5).flatten()))

    print(Counter((em.predict(emo_test_x[test_y == 0]) > 0.5).flatten()))
    print(Counter((em.predict(emo_test_x[test_y == 1]) > 0.5).flatten()))

    l_x = getOutput(language_model, train_iter)
    u_x = um.predict(tran_train_x)
    e_x = em.predict(emo_train_x)

    x = np.hstack([l_x, u_x, e_x])

    language_output = getOutput(language_model, test_iter)
    um_out = um.predict(tran_test_x)
    em_out = em.predict(emo_test_x)
    inp = np.hstack([language_output, um_out, em_out])

    model = get_model()
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x, train_y, epochs=100)
    model.evaluate(inp, test_y)

    print(Counter((model.predict(inp[test_y == 0]) > 0.5).flatten()))
    print(Counter((model.predict(inp[test_y == 1]) > 0.5).flatten()))
