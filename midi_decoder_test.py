import pretty_midi
from music import midi_io

midi_data = pretty_midi.PrettyMIDI("MidiFiles/liszt/liz_donjuan.mid")

mid = midi_io.midi_to_sequence_proto(midi_data)

print(mid.tracks[0].name)

current = 0
print(mid.tracks[0].notes[0].pitch)

for i in mid.tracks[0].notes:
    if i.pitch == 98:
        print(i.start_tick)
