from pretty_midi import PrettyMIDI
import fnmatch
import os
import numpy as np

NUM_KEYS = 88


def get_pitch(note):
    pitch = note.pitch - 21
    if pitch < 0 or pitch > 87:
        raise ValueError("pitch is not in piano range.")
    return pitch


def get_numerator(time_signature):
    numerator = time_signature.numerator
    return numerator


def get_denominator(time_signature):
    denominator = time_signature.denominator
    return denominator


class MidiProcessor(object):
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

    @staticmethod
    def embed_note(midi, note, piano_roll):
        start = midi.time_to_tick(note.start) // (midi.resolution // 4)
        end = midi.time_to_tick(note.end) // (midi.resolution // 4)
        for i in range(end - start):
            if i == 0:
                piano_roll[start][get_pitch(note)][0] = 1
            else:
                piano_roll[start + i][get_pitch(note)][1] = 1

    def get_all_piano_roll(self):
        piano_roll_list = []
        midi_list = self.get_midi_file_list()
        for midi in midi_list:
            piano_roll_length = midi.time_to_tick(midi.get_end_time()) // (midi.resolution // 4)

            for instrument in midi.instruments:
                piano_roll = np.zeros((piano_roll_length, NUM_KEYS, 2), dtype=np.int8)
                for note in instrument.notes:
                    self.embed_note(midi, note, piano_roll)
                piano_roll_list.append(piano_roll)

        return piano_roll_list

    def get_two_hand_piano_roll(self):
        right_hand = []
        left_hand = []
        midi_list = self.get_midi_file_list()
        for midi in midi_list:
            piano_roll_length = midi.time_to_tick(midi.get_end_time()) // (midi.resolution // 4)

            for instrument in midi.instruments:
                if instrument.name == "Piano right" and not instrument.is_drum:
                    piano_roll = np.zeros((piano_roll_length, NUM_KEYS, 2), dtype=np.int8)
                    for note in instrument.notes:
                        self.embed_note(midi, note, piano_roll)
                    right_hand.append(piano_roll)

                elif instrument.name == "Piano left" and not instrument.is_drum:
                    piano_roll = np.zeros((piano_roll_length, NUM_KEYS, 2), dtype=np.int8)
                    for note in instrument.notes:
                        self.embed_note(midi, note, piano_roll)
                    left_hand.append(piano_roll)

        return right_hand, left_hand
