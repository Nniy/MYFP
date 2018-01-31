
from music import note_sequence_io
x = 0
for i in note_sequence_io.note_sequence_record_iterator(
        "/private/tmp/melody_rnn/sequence_examples/training_melodies.tfrecord"):
    print(i)
