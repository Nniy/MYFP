import hashlib
import tensorflow as tf


def generate_note_sequence_id(filename, collection_name, source_type):
    filename_fingerprint = hashlib.sha1(filename.encode('utf-8'))
    return '/id/%s/%s/%s' % (
        source_type.lower(), collection_name, filename_fingerprint.hexdigest())


class NoteSequenceRecordWriter(tf.python_io.TFRecordWriter):
    def write(self, note_sequence):
        tf.python_io.TFRecordWriter.write(self, note_sequence.SerializeToString())
