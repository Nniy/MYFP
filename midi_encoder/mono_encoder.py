from pretty_midi import PrettyMIDI
import fnmatch
import os
import numpy as np
import h5py

from rnn import constants

NUM_KEYS = constants.EVENTS
maxlen = constants.STEPS
step = 15


def get_piano_pitch(midi_pitch):
    piano_pitch = midi_pitch.pitch - 21
    # if piano_pitch < 0 or piano_pitch > 87:
    #     raise ValueError("piano pitch is not in range.")
    return piano_pitch


def get_midi_file_list(midi_dir):
    midi_list = []
    for root, dirs, files in os.walk(midi_dir):
        for file in files:
            if fnmatch.fnmatch(file, "*.mid"):
                midi_filename = os.path.join(root, file)
                pretty_midi = PrettyMIDI(midi_filename)
                midi_list.append(pretty_midi)
    return midi_list


def get_all_piano_roll(midi_dir):
    print('reading from midi_dir...')
    inputs = []
    labels = []
    midi_list = get_midi_file_list(midi_dir)

    for midi in midi_list:
        piano_roll_length = midi.time_to_tick(midi.get_end_time()) // (midi.resolution // 4)
        for instrument in midi.instruments:
            roll = np.zeros((piano_roll_length, NUM_KEYS))
            mono_roll = np.zeros((piano_roll_length, NUM_KEYS))
            for note in instrument.notes:
                start = midi.time_to_tick(note.start) // (midi.resolution // 4)
                end = midi.time_to_tick(note.end) // (midi.resolution // 4)
                for i in range(end - start):
                    if i == 0:
                        roll[start][get_piano_pitch(note)] = note.velocity
                    else:
                        roll[start + i][-2] = 1

            tick = 0
            while tick < len(roll):
                if np.sum(roll[tick]) == 0:
                    mono_roll[tick][-1] = 1
                    tick += 1
                    if tick < len(roll):
                        while np.sum(roll[tick]) == 0:
                            if tick + 1 < len(roll):
                                mono_roll[tick][-2] = 1
                                tick += 1
                            else:
                                break
                elif roll[tick][-2] == 1:
                    mono_roll[tick][-2] = 1
                    tick += 1
                else:
                    mono_roll[tick][np.argmax(roll[tick])] = 1
                    tick += 1

            for j in range(0, len(mono_roll) - maxlen - 1, step):
                tmp = mono_roll[j:j+maxlen]
                if np.sum(tmp) < (maxlen*0.8):
                    continue
                else:
                    inputs.append(tmp)
                    labels.append(mono_roll[j+maxlen])

    return inputs, labels


x, y = get_all_piano_roll('/Users/Zongyu/Desktop/MYFP/MidiFiles')

hf = h5py.File('train.h5', 'w')
hf.create_dataset('x', data=x)
hf.create_dataset('y', data=y)
hf.close()
