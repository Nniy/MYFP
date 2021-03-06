from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import SimpleRNN
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt

import h5py
import numpy as np
import keras

import constants


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
model.add(SimpleRNN(128, input_shape=(maxlen, KEYS)))
model.add(Dense(KEYS))
model.add(Activation('softmax'))

TB = TensorBoard(log_dir='../cnn/logs/rnn')

op = keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=0.001, decay=0.95)


model.compile(loss='categorical_crossentropy', optimizer=op, metrics=['accuracy'])

fit = model.fit(x_train, y_train, batch_size=128, epochs=50, callbacks=[TB], validation_split=0.2)

print(fit.history.keys())
plt.plot(fit.history['loss'])
plt.plot(fit.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

model.save("model_rnn.h5")
model.save_weights("model_weights_rnn.h5")


