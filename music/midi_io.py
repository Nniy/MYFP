import six
import sys
import pretty_midi

from protobuf import music_pb2


class MIDIConversionError(Exception):
    pass


def midi_to_sequence_proto(midi_data):
    if isinstance(midi_data, pretty_midi.PrettyMIDI):
        midi = midi_data
    else:
        try:
            midi = pretty_midi.PrettyMIDI(six.BytesIO(midi_data))
        except:
            raise MIDIConversionError('Midi decoding error %s: %s' %
                                      (sys.exc_info()[0], sys.exc_info()[1]))
    sequence = music_pb2.PianoRoll()
    sequence.resolution = midi.resolution
    sequence.total_tick = midi.time_to_tick(midi.get_end_time()) // (midi.resolution // 4)

    for midi_track in midi.instruments:
        track = sequence.tracks.add()
        track.name = midi_track.name
        for midi_note in midi_track.notes:
            note = track.notes.add()
            note.velocity = midi_note.velocity
            note.pitch = midi_note.pitch
            note.start_tick = midi.time_to_tick(midi_note.start) // (midi.resolution // 4)
            note.end_tick = midi.time_to_tick(midi_note.end) // (midi.resolution // 4)

    return sequence
