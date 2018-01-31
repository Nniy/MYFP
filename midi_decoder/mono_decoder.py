import pretty_midi
import numpy as np

TICK_PER_SECOND = 0.1
end_of_piano_roll = np.ones(90)


def get_midi_pitch(piano_pitch):
    midi_pitch = piano_pitch + 21
    # if midi_pitch < 21 or midi_pitch > 108:
    #     raise ValueError("midi pitch is not in range.")
    return midi_pitch


def piano_roll_to_midi(piano_roll, filename):
    midi_output = pretty_midi.PrettyMIDI()
    midi_instrument = pretty_midi.Instrument(program=0)

    tick = 0
    while tick < len(piano_roll):
        if piano_roll[tick][-1] == 1:
            tick += 1
            if tick < len(piano_roll):
                while piano_roll[tick][-2] == 1:
                    if tick + 1 < len(piano_roll):
                        tick += 1
                    else:
                        tick += 1
                        break
        else:
            key = np.argmax(piano_roll[tick])
            start_time = tick
            end_time = tick + 1
            tick += 1
            if tick < len(piano_roll):
                while piano_roll[tick][-2] == 1:
                    if tick + 1 < len(piano_roll):
                        end_time += 1
                        tick += 1
                    else:
                        end_time += 1
                        tick += 1
                        break

            note = pretty_midi.Note(velocity=100,
                                    pitch=get_midi_pitch(key),
                                    start=start_time * TICK_PER_SECOND,
                                    end=end_time * TICK_PER_SECOND)
            midi_instrument.notes.append(note)

    midi_output.instruments.append(midi_instrument)
    midi_output.write(filename)
