import pretty_midi
from music import midi_io

midi = pretty_midi.PrettyMIDI("midi_encoder/chp_op18.mid")
output = midi_io.midi_to_proto(midi)

print(output.tracks[0].notes[0].start_tick)
