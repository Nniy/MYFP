import pretty_midi
import numpy as np

TICK_PER_SECOND = 0.1
empty_array = np.zeros(88, dtype=np.int8)


def get_midi_pitch(piano_pitch):
    midi_pitch = piano_pitch + 21
    if midi_pitch < 21 or midi_pitch > 108:
        raise ValueError("midi pitch is not in range.")
    return midi_pitch


class MonoDecoder(object):
    def __init__(self, piano_roll):
        self._piano_roll = piano_roll

    def piano_roll_to_midi(self, filename):
        midi_output = pretty_midi.PrettyMIDI()
        midi_instrument = pretty_midi.Instrument(program=0)

        for tick_idx in range(len(self._piano_roll)):
            if not np.array_equal(self._piano_roll[tick_idx][:-1], empty_array):
                key_idx = np.argmax(self._piano_roll[tick_idx][:-1])
                key_hold = 1
                start_time = tick_idx
                end_time = start_time + 1
                if (tick_idx + key_hold) in range(len(self._piano_roll)):
                    while self._piano_roll[tick_idx + key_hold][-1] == 1:
                        key_hold += 1
                        end_time += 1
                        if not ((tick_idx + key_hold) in range(len(self._piano_roll))):
                            break
                    note = pretty_midi.Note(velocity=100,
                                            pitch=get_midi_pitch(key_idx),
                                            start=start_time*TICK_PER_SECOND,
                                            end=end_time*TICK_PER_SECOND)
                    midi_instrument.notes.append(note)

        midi_output.instruments.append(midi_instrument)
        midi_output.write(filename)
