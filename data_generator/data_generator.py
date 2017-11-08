from midi_encoder import midi_encoder
import numpy as np
import h5py

MIDI_DIR = "../MidiFiles"

data = midi_encoder.MidiEncoder(MIDI_DIR)
piano_roll_list = data.get_all_piano_roll()


def split_piano_roll(roll_list, split_length):
    result = np.zeros((0, split_length, 88, 2))
    for roll in roll_list:
        divided_num = len(roll) // split_length
        if len(roll) % split_length != 0:
            roll = roll[:-(len(roll) % split_length)]
        roll = np.split(roll, divided_num)
        roll = np.array(roll, dtype=np.int8)
        result = np.append(result, roll, axis=0)
        print(result.shape)
    print("Splitting...")
    split = np.split(result, [0, split_length-1], axis=1)
    print("Splitting done")
    inputs = split[1]
    labels = split[2]
    return inputs, labels


x, y = split_piano_roll(piano_roll_list, 30)

hf = h5py.File("train_data.h5", "w")
hf.create_dataset("inputs", data=x)
hf.create_dataset("labels", data=y)
hf.close()
print(x.shape, y.shape)
