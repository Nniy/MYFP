from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten

import h5py
import numpy as np
import keras


def read_from_file(filename):
    hf = h5py.File(filename, "r")
    x = np.array(hf.get("x"))
    y = np.array(hf.get("y"))
    return x, y


x, y = read_from_file('/Users/Zongyu/Desktop/MYFP/midi_encoder/train_cnn.h5')
x_train = x[:-15000]
x_test = x[-15000:]
y_train = y[:-15000]
y_test = y[-15000:]
x_train = x_train.reshape(x_train.shape[0], 90, 90, 1)
x_test = x_test.reshape(x_test.shape[0], 90, 90, 1)

print('Build model...')
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(90, 90, 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(90, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=128,
          epochs=10,
          verbose=1,
          validation_data=(x_test, y_test))

model.save("model.h5")
model.save_weights("model_weights.h5")
