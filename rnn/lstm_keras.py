from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, Dropout
from keras.callbacks import TensorBoard

import h5py
import numpy as np

import constants
import keras


def read_from_file(filename):
    hf = h5py.File(filename, "r")
    x = np.array(hf.get("x"))
    y = np.array(hf.get("y"))
    return x, y


x_train, y_train = read_from_file('/Users/Zongyu/Desktop/MYFP/midi_encoder/train.h5')
KEYS = constants.EVENTS
maxlen = constants.STEPS

print('Build model...')
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(maxlen, KEYS)))
model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(Dense(KEYS, activation='softmax'))

TB = TensorBoard(log_dir='../cnn/logs/lstm_drop_best_2_layers')


op = keras.optimizers.Adam(lr=0.5, beta_1=0.9, beta_2=0.999, epsilon=0.001, decay=0.85)
model.compile(loss='categorical_crossentropy', optimizer=op, metrics=['accuracy'])

fit = model.fit(x_train, y_train, batch_size=128, epochs=50, callbacks=[TB], validation_split=0.2)

model.save("model.h5")
model.save_weights("model_weights.h5")
