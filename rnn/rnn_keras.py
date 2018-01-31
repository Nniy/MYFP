from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop

import h5py
import numpy as np

from rnn import constants


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
model.add(LSTM(128, input_shape=(maxlen, KEYS)))
model.add(Dense(KEYS))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model.fit(x_train, y_train,
          batch_size=128,
          epochs=10)

model.save("model.h5")
model.save_weights("model_weights.h5")
