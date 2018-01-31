import os
import sys
import time

import numpy as py
import tensorflow as tf


def make_rnn_cell(rnn_layer_sizes, dropout_keep_prob=1.0, attn_length=0, base_cell=tf.contrib.rnn.BasicLSTMCell):
    cells = []
    for num_units in rnn_layer_sizes:
        cell = base_cell(num_units)
        if attn_length and not cells:
            cell = tf.contrib.rnn.AttentionCellWrapper(cell, attn_length, state_is_tuple=True)
        cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=dropout_keep_prob)
        cells.append(cell)
    cell = tf.contrib.rnn.MultiRNNCell(cells)

    return cell

def build_graph(mode, config, sequence_example_file_paths=None):
    if mode not in ('train', 'eval', 'generate'):
        raise ValueError('Not valid mode.')

    hparams = config.hparams


