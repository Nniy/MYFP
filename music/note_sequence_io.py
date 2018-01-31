import hashlib
import tensorflow as tf

from protobuf import music_pb2


def generate_note_sequence_id(filename, collection_name, source_type):
    filename_fingerprint = hashlib.sha1(filename.encode('utf-8'))
    return '/id/%s/%s/%s' % (
        source_type.lower(), collection_name, filename_fingerprint.hexdigest())


def note_sequence_record_iterator(path):
    reader = tf.python_io.tf_record_iterator(path)
    for serialized_sequence in reader:
        yield music_pb2.PianoRoll.FromString(serialized_sequence)


class NoteSequenceRecordWriter(tf.python_io.TFRecordWriter):
    def write(self, note_sequence):
        tf.python_io.TFRecordWriter.write(self, note_sequence.SerializeToString())
