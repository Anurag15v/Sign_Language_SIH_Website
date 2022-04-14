import pickle
import tensorflow as tf
import numpy as np
import os
import itertools

def makemodel(num_labels):
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(88)),
        tf.keras.layers.LayerNormalization(-1),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(num_labels, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def main():
    X = []
    y = []
    labels = []
    for i in os.listdir("./gestures"):
        labels.append(i[:-4])
        with open("./gestures/{}".format(i), "rb") as f:
            data = pickle.load(f)
        for j in data:
            X.append(j)
            y.append(len(labels)-1)
    with open("labels.pkl", "wb") as f:
        pickle.dump(labels, f)
    X = np.array(X, dtype=np.float64)
    print(X.shape)
    y = np.array(y, dtype = np.float64).reshape((len(y), 1))
    print(y.shape)
    model = makemodel(len(labels))
    model.fit(X, y, epochs=100, validation_split=0.1, callbacks=[tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)])
    model.save("my_model")

if __name__ == '__main__':
    main()