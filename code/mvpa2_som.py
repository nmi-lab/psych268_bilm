#!/bin/python
#-----------------------------------------------------------------------------
# File Name : mvpa2_som.py
# Author: pyMVPA
#
# Creation Date : Thu 03 Nov 2016 02:05:53 PM PDT
# Last Modified : 
#
# Copyright : (c) Hanke et al
# Licence : GPLv2
#----------------------------------------------------------------------------- 
#Modified from som.py in pyMVPA2 source
from mvpa2.suite import *
colors = np.array(
         [[0., 0., 0.],
          [0., 0., 1.],
          [0., 0., 0.5],
          [0.125, 0.529, 1.0],
          [0.33, 0.4, 0.67],
          [0.6, 0.5, 1.0],
          [0., 1., 0.],
          [1., 0., 0.],
          [0., 1., 1.],
          [1., 0., 1.],
          [1., 1., 0.],
          [1., 1., 1.],
          [.33, .33, .33],
          [.5, .5, .5],
          [.66, .66, .66]])

# store the names of the colors for visualization later on
color_names = \
        ['black', 'blue', 'darkblue', 'skyblue',
         'greyblue', 'lilac', 'green', 'red',
         'cyan', 'violet', 'yellow', 'white',
         'darkgrey', 'mediumgrey', 'lightgrey']
som = SimpleSOMMapper((20, 30), 400, learning_rate=0.05)
som.train(colors)
pl.imshow(som.K, origin='lower')
