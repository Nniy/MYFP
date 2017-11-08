import pretty_midi
import numpy as np

TICK_PER_SECOND = 0.15


def get_midi_pitch(piano_pitch):
    midi_pitch = piano_pitch + 21
    if midi_pitch < 21 or midi_pitch > 108:
        raise ValueError("midi pitch is not in range.")
    return midi_pitch


class MidiDecoder(object):
    def __init__(self, piano_roll):
        self._piano_roll = piano_roll

    def piano_roll_to_midi(self):
        midi_output = pretty_midi.PrettyMIDI()
        midi_instrument = pretty_midi.Instrument(program=0)

        for tick_idx in range(len(self._piano_roll)):
            for key_idx in range(88):
                if np.array_equal(self._piano_roll[tick_idx][key_idx], [1, 1]):
                    key_hold = 1
                    start_time = tick_idx
                    end_time = start_time + 1
                    while np.array_equal(self._piano_roll[tick_idx + key_hold][key_idx], [1, 0]):
                        key_hold += 1
                        end_time += 1
                    note = pretty_midi.Note(velocity=100,
                                            pitch=get_midi_pitch(key_idx),
                                            start=start_time*TICK_PER_SECOND,
                                            end=end_time*TICK_PER_SECOND)
                    midi_instrument.notes.append(note)

        midi_output.instruments.append(midi_instrument)
        midi_output.write("../midi_from_decoder.mid")
