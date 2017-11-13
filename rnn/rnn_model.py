
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint
import numpy as np
import h5py

hf = h5py.File("../data_generator/mono_speedy_data.h5", "r")
x_train = hf.get("inputs")
y_train = hf.get("labels")
x_train = np.array(x_train, dtype=np.int8)
y_train = np.array(y_train, dtype=np.int8)
y_train = np.reshape(y_train, (len(y_train), 88))

max_features = 88
maxlen = 35
batch_size = 128

print('Build model...')
model = Sequential()
model.add(LSTM(128, dropout=0.5, return_sequences=True, input_shape=(maxlen, max_features)))
model.add(LSTM(128, dropout=0.5))
model.add(Dense(max_features, activation='sigmoid'))
model.add(Activation('softmax'))
# try using different optimizers and different optimizer configs
optimizer = Adam(lr=0.001, clipnorm=5)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)
model.save("rnn.h5")

tensorboard_cb = TensorBoard(log_dir='./logs', histogram_freq=0,
                             write_graph=True, write_images=True)
checkpoint_cb = ModelCheckpoint("./model_weights_cp.h5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')

model.fit(x_train, y_train,
          batch_size=batch_size,
          validation_split=0.2,
          epochs=10, callbacks=[checkpoint_cb, tensorboard_cb])
model.save_weights("./model_weights.h5")
