import tensorflow.keras as keras


def get_emotion_model():
    return keras.Sequential([
        keras.layers.Dense(32, input_shape=(4,), activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.25),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ]
)