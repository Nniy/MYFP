from keras.models import load_model
import h5py
import numpy as np

from midi_decoder import mono_decoder


np.set_printoptions(threshold=np.inf)
model = load_model("rnn.h5")
model.load_weights("model_weights.h5")
hf = h5py.File("../data_generator/mono_speedy_data.h5", "r")
primer = hf.get("inputs")
primer = np.array(primer, dtype=np.int8)
preds = primer[0].reshape((1, 35, 88))
piano_roll = primer[0]

for i in range(100):
    empty = np.zeros((1, 1, 88))
    predictions = model.predict(preds)[0]
    key_idx = np.argmax(predictions)
    empty[0][0][key_idx] = 1
    piano_roll = np.append(piano_roll, empty[0], axis=0)
    preds = np.append(preds, empty, axis=1)
    preds = preds[0][1:][:]
    preds = np.reshape(preds, (1, 35, 88))

mono_decoder.MonoDecoder(primer[0]).piano_roll_to_midi("primer.mid")
mono_decoder.MonoDecoder(piano_roll).piano_roll_to_midi("predict.mid")
