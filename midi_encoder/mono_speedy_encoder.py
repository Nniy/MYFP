from pretty_midi import PrettyMIDI
import fnmatch
import os
import numpy as np

NUM_KEYS = 88
empty_array = np.zeros(88, dtype=np.int8)


def get_piano_pitch(midi_pitch):
    piano_pitch = midi_pitch.pitch - 21
    if piano_pitch < 0 or piano_pitch > 87:
        raise ValueError("piano pitch is not in range.")
    return piano_pitch


def embed_note(midi, note, piano_roll):
    start = midi.time_to_tick(note.start) // (midi.resolution // 4)
    end = midi.time_to_tick(note.end) // (midi.resolution // 4)
    for i in range(end - start):
        piano_roll[start + i][get_piano_pitch(note)] = 1


class MonoSpeedyEncoder(object):
    def __init__(self, midi_dir):
        self._midi_dir = midi_dir

    def get_midi_file_list(self):
        midi_list = []
        for root, dirs, files in os.walk(self._midi_dir):
            for file in files:
                if fnmatch.fnmatch(file, "*.mid"):
                    midi_filename = os.path.join(root, file)
                    pretty_midi = PrettyMIDI(midi_filename)
                    midi_list.append(pretty_midi)
        return midi_list

    def get_all_piano_roll(self):
        piano_roll_list = []
        midi_list = self.get_midi_file_list()
        for midi in midi_list:
            piano_roll_length = midi.time_to_tick(midi.get_end_time()) // (midi.resolution // 4)

            for instrument in midi.instruments:
                piano_roll = np.zeros((piano_roll_length, NUM_KEYS), dtype=np.int8)
                for note in instrument.notes:
                    embed_note(midi, note, piano_roll)
                piano_roll_list.append(piano_roll)

        return piano_roll_list
