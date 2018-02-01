from keras.models import load_model
import numpy as np
import h5py

from midi_decoder import mono_decoder


np.set_printoptions(threshold=np.inf)
model = load_model("model.h5")
model.load_weights("model_weights.h5")


hf = h5py.File('/Users/Zongyu/Desktop/MYFP/midi_encoder/train_cnn.h5', "r")
x = np.array(hf.get("x"))[0]
sequence = []
for i in x:
    sequence.append(np.argmax(i))
generated = sequence


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probability = np.random.multinomial(1, preds, 1)
    return np.argmax(probability)


for _ in range(600):
    piano_roll = np.zeros((1, 90, 90, 1))
    for t, note in enumerate(generated):
        piano_roll[0, t, note, 0] = 1

    predictions = model.predict(piano_roll, verbose=0)[0]
    next_index = sample(predictions)

    sequence.append(next_index)
    generated = sequence[-90:]

result = np.zeros((690, 90))
for t, note in enumerate(sequence):
    result[t, note] = 1


mono_decoder.piano_roll_to_midi(result, 'generated.mid')
