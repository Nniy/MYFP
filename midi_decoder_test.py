import pretty_midi
import numpy as np
np.set_printoptions(threshold=np.inf)

# # Create a PrettyMIDI object
# cello_c_chord = pretty_midi.PrettyMIDI()
# # Create an Instrument instance for a cello instrument
# cello_program = pretty_midi.instrument_name_to_program('Cello')
# cello = pretty_midi.Instrument(program=cello_program)
# # Iterate over note names, which will be converted to note number later
# time = 0
# for note_name in ['C5', 'C5', 'C5']:
#     # Retrieve the MIDI note number for this note name
#     note_number = pretty_midi.note_name_to_number(note_name)
#     # Create a Note instance, starting at 0s and ending at .5s
#     note = pretty_midi.Note(
#         velocity=100, pitch=note_number, start=time, end=(time + 0.5))
#     # Add it to our cello instrument
#     cello.notes.append(note)
#     time += 0.5
# # Add the cello instrument to the PrettyMIDI object
# cello_c_chord.instruments.append(cello)
# # Write out the MIDI data
# cello_c_chord.write('cello-C-chord.mid')
#
# mid = pretty_midi.PrettyMIDI("/Users/Zongyu/Desktop/MYFP/MidiFiles/beeth/beethoven_opus10_1.mid")
# print(mid.instruments)
# # a = mid.instruments[0].get_piano_roll()
# # print(a)
# # b = np.zeros((100, 30, 88, 2))
# # c = np.split(b, [0, 29], axis=1)
# # a = np.zeros((12, 2, 3, 5))
# # a = np.split(b, 50)
# # d = [1, 2, 0]
# # d = np.array(d, dtype=np.bool)
# # d[0] = d[0] + 2
# # print(d)
# a = np.zeros((10, 2))
# b = np.array([[1,2,3,4], [4,5,6,7]])
# print(b[1][:-1])
# print(2 in range(3))

a = np.zeros((1, 1, 5))
b = np.ones((1, 3, 5))

b = np.append(b, a, axis=1)
print(b[1][3][4])



