import os
import tensorflow as tf

from music import midi_io
from music import note_sequence_io

# FLAGS = tf.app.flags.FLAGS
#
# tf.app.flags.DEFINE_string('input_dir', None,
#                            'Directory containing files to convert.')
# tf.app.flags.DEFINE_string('output_file', None,
#                            'Path to output TFRecord file. Will be overwritten '
#                            'if it already exists.')
# tf.app.flags.DEFINE_bool('recursive', False,
#                          'Whether or not to recurse into subdirectories.')
# tf.app.flags.DEFINE_integer('num_threads', 1,
#                             'Number of worker threads to run in parallel.')
# tf.app.flags.DEFINE_string('log', 'INFO',
#                            'The threshold for what messages will be logged '
#                            'DEBUG, INFO, WARN, ERROR, or FATAL.')


def convert_files(root_dir, sub_dir, writer, recursive=False):
    dir_to_convert = os.path.join(root_dir, sub_dir)
    tf.logging.info("Converting files in '%s'.", dir_to_convert)
    files_in_dir = tf.gfile.ListDirectory(os.path.join(dir_to_convert))
    recurse_sub_dirs = []
    written_count = 0
    for file_in_dir in files_in_dir:
        tf.logging.log_every_n(tf.logging.INFO,
                               '%d files converted.',
                               1000,
                               written_count)
        full_file_path = os.path.join(dir_to_convert, file_in_dir)
        if (full_file_path.lower().endswith('.mid') or
                full_file_path.lower().endswith('.midi')):
            try:
                sequence = convert_midi(root_dir, sub_dir, full_file_path)
            except Exception as exc:
                tf.logging.fatal('%r generated an exception: %s', full_file_path, exc)
                continue
            if sequence:
                writer.write(sequence)
        else:
            if recursive and tf.gfile.IsDirectory(full_file_path):
                recurse_sub_dirs.append(os.path.join(sub_dir, file_in_dir))
            else:
                tf.logging.warning(
                    'Unable to find a converter for file %s', full_file_path)
        for recurse_sub_dir in recurse_sub_dirs:
            convert_files(root_dir, recurse_sub_dir, writer)


def convert_midi(root_dir, sub_dir, full_file_path):
    try:
        sequence = midi_io.midi_to_sequence_proto(
            tf.gfile.FastGFile(full_file_path, 'rb').read())
    except midi_io.MIDIConversionError as e:
        tf.logging.warning(
            'Could not parse MIDI file %s. It will be skipped. Error was: %s',
            full_file_path, e)
        return None
    sequence.collection_name = os.path.basename(root_dir)
    sequence.filename = os.path.join(sub_dir, os.path.basename(full_file_path))
    sequence.id = note_sequence_io.generate_note_sequence_id(
        sequence.filename, sequence.collection_name, 'midi')
    tf.logging.info('Converted MIDI file %s.', full_file_path)
    return sequence


def convert_directory(root_dir, output_file, recursive=False):
    with note_sequence_io.NoteSequenceRecordWriter(output_file) as writer:
        convert_files(root_dir, '', writer, recursive)


convert_directory("/Users/Zongyu/Desktop/MYFP/MidiFiles/",
                  "/Users/Zongyu/Desktop/MYFP/midi_data/midi_data.tfrecord",
                  recursive=True)

# def main(_):
#     tf.logging.set_verbosity(FLAGS.log)
#
#     if not FLAGS.input_dir:
#         tf.logging.fatal('--input_dir required')
#         return
#     if not FLAGS.output_file:
#         tf.logging.fatal('--output_file required')
#         return
#
#     input_dir = os.path.expanduser(FLAGS.input_dir)
#     output_file = os.path.expanduser(FLAGS.output_file)
#     output_dir = os.path.dirname(output_file)
#
#     if output_dir:
#         tf.gfile.MakeDirs(output_dir)
#
#     convert_directory(input_dir, output_file, FLAGS.recursive)
#
#
# def console_entry_point():
#     tf.app.run(main)
#
#
# if __name__ == '__main__':
#     console_entry_point()
