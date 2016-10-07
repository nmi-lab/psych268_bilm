#!/bin/python
#-----------------------------------------------------------------------------
# Author: Emre Neftci
#
# Creation Date : 20-04-2016
# Last Modified : Thu 06 Oct 2016 11:56:37 PM PDT
#
# Copyright : (c) 
# Licence : GPLv2
#----------------------------------------------------------------------------- 

from npamlib import *

#Load digits 3 and 8 only
data, labels = data_load_mnist([3,8])

#convert labels to True / False
labelsTF = (labels==labels[0])
#Train a data sample with trained perceptron:
w, res = ann_train_perceptron(data[:100], labelsTF[:100], n = 1000, eta = .1)

wbias = w[0]
wdata = w[1:]

#Test a data sample with trained perceptron:
print(ann_perceptron(data[0],w))

#Show stimulus
stim_show(data)

