from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt


import h5py
import numpy as np
import keras


def read_from_file(filename):
    hf = h5py.File(filename, "r")
    x_ = np.array(hf.get("x"))
    y_ = np.array(hf.get("y"))
    return x_, y_


x, y = read_from_file('/Users/Zongyu/Desktop/MYFP/midi_encoder/train_cnn.h5')
x = x.reshape(x.shape[0], 90, 90, 1)

print('Build model...')
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(90, 90, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(90, activation='softmax'))

TB = TensorBoard(log_dir='./logs/cnn')

op = keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=0.001, decay=0.95)


model.compile(loss="categorical_crossentropy",
              optimizer=op,
              metrics=['accuracy'])

fit = model.fit(x, y,
                batch_size=128,
                epochs=50,
                verbose=1,
                validation_split=0.2,
                callbacks=[TB])


print(fit.history.keys())
plt.plot(fit.history['loss'])
plt.plot(fit.history['val_loss'])
plt.title('Training curves')
plt.ylabel('Cross-entropy loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

plt.plot(fit.history['acc'])
plt.plot(fit.history['val_acc'])
plt.title('Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

model.save("model.h5")
model.save_weights("model_weights.h5")
