import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow.keras as keras


def get_user_model():
    return keras.Sequential([
        keras.layers.Dense(32, input_shape=(9,), activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(128, activation='relu'),

        keras.layers.Dropout(0.25),

        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')

    ])


if __name__ == '__main__':
    features = ["comment_number", "thumb_number", "repost_number", "is_certified", "follow_number", "fan_number",
                "weibo_number", 'label']

    data = pd.read_excel("C:/Users/74098/PycharmProjects/weibo/weibo_new-1.xlsx")
    data = data[features]

    data = data.dropna().astype('float64')

    x, y = data[features[:-1]], data['label']

    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.1, random_state=42)

    scaler = StandardScaler()
    scaler.fit(train_x)
    train_x = scaler.transform(train_x)
    test_x = scaler.transform(test_x)

    model = get_user_model()

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(train_x, train_y, epochs=100, callbacks=[keras.callbacks.EarlyStopping(patience=5, min_delta=1e-3)])
    model.evaluate(test_x, test_y)

    print(model.predict(test_x[test_y == 0]))
    # from collections import Counter
    #
    # print(Counter((model.predict(test_x[test_y == 0]) > 0.5).flatten()))
    # print(Counter((model.predict(test_x[test_y == 1]) > 0.5).flatten()))
