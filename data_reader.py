import numpy as np
import h5py

np.set_printoptions(threshold=np.inf)

hf = h5py.File("data_generator/mono_speedy_data.h5", "r")
x_train = hf.get("inputs")
y_train = hf.get("labels")

# for i in range(len(x_train)):
#     print(np.array_equal(x_train[i], x_train[i+1]), i)

print(x_train[0], x_train[1])
