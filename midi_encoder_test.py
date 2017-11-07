from midi_encoder import midi_encoder
from midi_decoder import midi_decoder
from pretty_midi import PrettyMIDI
import numpy as np
np.set_printoptions(threshold=np.inf)

# mid2 = PrettyMIDI("/Users/Zongyu/PycharmProjects/lark/MidiFiles/Sinding/fruehlingsrauschen_format0.mid")

mid1 = midi_encoder.MidiEncoder("/Users/Zongyu/Desktop/MYFP/midi_encoder")
# print(mid1.get_midi_file_list())
a = mid1.get_all_piano_roll()

midi_decoder.MidiDecoder(a[0]).piano_roll_to_midi()
# for note in mid2.instruments[0].notes:
#     print(mid2.time_to_tick(note.start) // (mid2.resolution // 4), mid2.time_to_tick(note.end) // (mid2.resolution // 4))

# # Create a PrettyMIDI object
# cello_c_chord = pretty_midi.PrettyMIDI()
# # Create an Instrument instance for a cello instrument
# cello_program = pretty_midi.instrument_name_to_program('Cello')
# cello = pretty_midi.Instrument(program=cello_program)
# # Iterate over note names, which will be converted to note number later
# for note_name in ['C5', 'E5', 'G5']:
#     # Retrieve the MIDI note number for this note name
#     note_number = pretty_midi.note_name_to_number(note_name)
#     # Create a Note instance, starting at 0s and ending at .5s
#     note = pretty_midi.Note(
#         velocity=100, pitch=note_number, start=0, end=.5)
#     # Add it to our cello instrument
#     cello.notes.append(note)
# # Add the cello instrument to the PrettyMIDI object
# cello_c_chord.instruments.append(cello)
# # Write out the MIDI data
# cello_c_chord.write('cello-C-chord.mid')

# midi = PrettyMIDI("cello-C-chord.mid")
# print(midi.time_to_tick(midi.get_end_time()) // midi.resolution)
# print(midi.time_to_tick(midi.instruments[0].notes[0].end) // midi.resolution)
# print(midi.instruments[0].notes[0].pitch)
# for i in range(88):
#     print(i)
# print(midi.get_end_time())
# print(midi.resolution)
# print(midi.time_to_tick(midi.get_end_time()))
# print(midi.time_to_tick(midi.get_end_time()) // midi.resolution)
# a = midi.tick_to_time(midi.resolution) * 290
# print(a)

# time_signatures = midi.time_signature_changes
# numerators = []
# denominators = []
# times = []
# end_time = midi.get_end_time()
# num_ticks = midi.time_to_tick(end_time)
#
# piano_roll_length = 0
#
# for time_signature in time_signatures:
#     numerators.append(time_signature.numerator)
#     denominators.append(time_signature.denominator)
#     times.append(time_signature.time)
#
# previous_num_beats = 0
# for i in range(len(times)):
#     piano_roll_length += (len(midi.get_beats(times[-i - 1])) - previous_num_beats) * 16 // denominators[-i - 1]
#     previous_num_beats = piano_roll_length // (16 // denominators[-i - 1])
# print(piano_roll_length)

# print(a.time_signature_changes)
# print(a.instruments[0].name)
# c = a.get_end_time()
# a.time_to_tick(c)
# print(len(a.get_beats()))

# mid = me.MidiProcessor("/Users/Zongyu/PycharmProjects/lark/MidiFiles/chopin/")
# a, b = mid.get_two_hand_instrument()
# print("left\n", len(a), a)
# print("right\n", len(b), b)

# @staticmethod
# def _read_from_file(filename):
#     midi_file = PrettyMIDI(filename)
#     return midi_file
#
#
# def _get_piano_roll(self, filename):
#     track = self._read_from_file(filename).instruments[RIGHT_HAND_TRACK]
#     piano_roll = track.get_piano_roll()[21:109]
#     result = piano_roll.T
#     return result
#
#
# def sample_from_piano_roll(self, filename):
#     piano_roll = self._get_piano_roll(filename)
#     input_array = np.array(piano_roll[0: SAMPLE_SIZE - 1])
#     label_array = np.array(piano_roll[SAMPLE_SIZE - 1])
#     assert len(input_array.shape) == 2
#     input_array = input_array.reshape(1, input_array.shape[0], input_array.shape[1])
#     label_array = label_array.reshape(1, label_array.shape[0])
#     current_index = 0
#     piano_roll_size = len(piano_roll)
#     while current_index <= piano_roll_size:
#         input_block = piano_roll[current_index: current_index + SAMPLE_SIZE - 1]
#         # TODO: End of piano deleted, solve later.
#         if input_block.shape[0] < SAMPLE_SIZE - 1:
#             break
#
#         label_block = piano_roll[current_index + SAMPLE_SIZE - 1]
#         input_block = input_block.reshape(1, input_block.shape[0], input_block.shape[1])
#         label_block = label_block.reshape(1, label_block.shape[0])
#         input_array = np.append(input_array, input_block, axis=0)
#         label_array = np.append(label_array, label_block, axis=0)
#
#         current_index += SAMPLE_SIZE
#
#     return input_array, label_array
