# -*- coding: utf-8 -*-
import tensorflow as tf

class CNNMainNetSRB(tf.keras.Model):
    def __init__(self, 
                 num_filters: int, 
                 dilation: list, 
                 skip_conv11: bool=False):
        super(CNNMainNetSRB, self).__init__(name='CNNMainNetSRB')
        # Layer normalization is done over conv 'channels' dimension
        self._layer_norm_1 = tf.keras.layers.LayerNormalization(axis=-1)
        self._conv_1 = tf.keras.layers.SeparableConv2D(filters=num_filters,
                                                       kernel_size=[3,3],
                                                       padding='same',
                                                       dilation_rate=dilation,
                                                       activation=None)
        # Layer normalization is done over conv 'channels' dimension
        self._layer_norm_2 = tf.keras.layers.LayerNormalization(axis=-1)
        self._conv_2 = tf.keras.layers.SeparableConv2D(filters=num_filters,
                                                       kernel_size=[3,3],
                                                       padding='same',
                                                       dilation_rate=dilation,
                                                       activation=None)
        if skip_conv11==True:
            self._skip_conv11 = tf.keras.layers.Conv2D(filters=num_filters,
                                                       kernel_size=[1,1],
                                                       padding='same',
                                                       activation=None)
        else:
            self._skip_conv11 = None

    def call(self, inputs, mode: str='final'):
        z = self._layer_norm_1(inputs)
        z = tf.nn.relu(z)
        z = self._layer_norm_2(self._conv_1(z))
        z = tf.nn.relu(z)
        middle_output = z
        z = self._conv_2(z) # [batch size, num_ofdm_symbols, fft_size, num_channels]
        if self._skip_conv11!=None:
            z = z + self._skip_conv11(inputs)
        else:
            z = z + inputs
        if mode=='final':
            return z
        else:
            return middle_output, z