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

mid = pretty_midi.PrettyMIDI("cello-C-chord.mid")
a = mid.instruments[0].get_piano_roll()
print(a)
