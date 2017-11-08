from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import adam
import numpy as np
import random

print("Build model...")
model = Sequential()
model.add(LSTM(100, input_shape=(29, 88)))
model.add(Dense(88))
model.add(Activation('softmax'))

optimizer = adam(lr=0.5, decay=0.00085)

model.compile(loss='categorical_crossentropy', optimizer=optimizer)
