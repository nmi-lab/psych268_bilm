#!/bin/python
#-----------------------------------------------------------------------------
# File Name : brain2_perceptron_learn.py
# Author: Emre Neftci
#
# Creation Date : Thu 06 Oct 2016 05:10:03 PM PDT
# Last Modified : Thu 06 Oct 2016 11:48:17 PM PDT
#
# Copyright : (c) UC Regents, Emre Neftci
# Licence : GPLv2
#----------------------------------------------------------------------------- 

from brian2 import *
from npamlib import *

def bin_rate(r_mon, duration):
    '''
    Calculates the mean rate of PopulationRateMonitor r_mon
    '''
    return np.array(r_mon.rate).reshape(-1, duration/defaultclock.dt).mean(axis=1)

n_samples = 100

#Neuron Parameters (modify these)
Cm = 50*pF; gl = 1e-9*siemens; taus = 20*ms
Vt = 10*mV; Vr = 0*mV;

#How long each stimulus was presented
duration = 200*ms

eqs = '''
dv/dt  = - gl*v/Cm 
         + isyn/Cm + Vt*gl/Cm: volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
'''

data, labels = ann_createDataSet(n_samples) #create 20 2d data samples
blabels = (labels+1)//2 #labels -1,1 to 0,1
data = (1+data)/2 #inputs in the range 0,1

#bias and weights (modify these)
wbias = 0.
wdata = [.1,.1]

## Spiking Network
#Following 2 lines for time-dependent inputs
rate = TimedArray(data*100*Hz, dt = duration)
Pdata = NeuronGroup(data.shape[1], 'rates = rate(t,i) : Hz', threshold='rand()<rates*dt')

#Input bias
Pbias = PoissonGroup(1, rates = 100*Hz)
P = NeuronGroup(1, eqs, threshold='v>Vt', reset='v = Vr',
                refractory=20*ms, method='milstein')

Sdata = Synapses(Pdata, P, 'w : amp', on_pre='isyn += w')
Sdata.connect() #Connect all-to-all
Sdata.w = wdata*nA

Sbias = Synapses(Pbias, P, 'w : amp', on_pre='isyn += w')
Sbias.connect() #Connect all-to-all
Sbias.w = wbias*nA

s_mon = SpikeMonitor(P)
r_mon = PopulationRateMonitor(P) #Monitor spike rates
s_mon_data = SpikeMonitor(Pdata)

run(n_samples*duration)

output_rate = bin_rate(r_mon, duration)

