from keras.models import load_model
import numpy as np
import h5py

from midi_decoder import mono_decoder
import constants

roll_length = constants.ROLL_LENGTH


np.set_printoptions(threshold=np.inf)
model = load_model("model.h5")
model.load_weights("model_weights.h5")


hf = h5py.File('/Users/Zongyu/Desktop/MYFP/midi_encoder/train.h5', "r")
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


for _ in range(roll_length):
    piano_roll = np.zeros((1, 50, 90))
    for t, note in enumerate(generated):
        piano_roll[0, t, note] = 1

    predictions = model.predict(piano_roll, verbose=0)[0]
    next_index = sample(predictions)

    sequence.append(next_index)
    generated = sequence[-50:]

result = np.zeros((roll_length + 50, 90))
for t, note in enumerate(sequence):
    result[t, note] = 1


mono_decoder.piano_roll_to_midi(result, 'generated_best_01.mid')
print(sequence)
# hf = h5py.File('piano_roll.h5', 'w')
# hf.create_dataset('piano_roll', data=sequence)
