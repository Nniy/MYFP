from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
import numpy as np
import random
import h5py

hf = h5py.File("../data_generator/mono_data.h5", "r")
x_train = hf.get("inputs")
y_train = hf.get("labels")
x_train = np.array(x_train, dtype=np.int8)
y_train = np.array(y_train, dtype=np.int8)
y_train = np.reshape(y_train, (len(y_train), 89))

max_features = 89
maxlen = 35
batch_size = 128

print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, 89)))
model.add(Dense(89, activation='sigmoid'))
model.add(Activation('softmax'))

# try using different optimizers and different optimizer configs
optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

for iteration in range(1, 60):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(x_train, y_train,
              batch_size=batch_size,
              validation_split=0.2,
              epochs=1)

# print("Build model...")
# model = Sequential()
# model.add(LSTM(128, input_shape=(35, 88)))
# model.add(Dense(88))
# model.add(Activation('softmax'))
#
# optimizer = adam(lr=0.5, decay=0.00085)
#
# model.compile(loss='categorical_crossentropy', optimizer=optimizer)
#
#
# def sample(preds, temperature=1.0):
#     # helper function to sample an index from a probability array
#     preds = np.asarray(preds).astype('float64')
#     preds = np.log(preds) / temperature
#     exp_preds = np.exp(preds)
#     preds = exp_preds / np.sum(exp_preds)
#     probas = np.random.multinomial(1, preds, 1)
#     return np.argmax(probas)
