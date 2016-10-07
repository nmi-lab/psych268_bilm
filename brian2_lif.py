#!/bin/python
#-----------------------------------------------------------------------------
# File Name : brian2_lif.py
# Author: Emre Neftci
#
# Creation Date : Wed 28 Sep 2016 12:05:29 PM PDT
# Last Modified : 
#
# Copyright : (c) UC Regents, Emre Neftci
# Licence : GPLv2
#----------------------------------------------------------------------------- 
#Modified from Brian2 documentation examples 
from brian2 import *

taum = 20*ms
Vt = -50*mV
Vr = -60*mV
El = -49*mV

eqs = '''
dv/dt  = -(v-El)/taum + xi/sqrt(ms)*mV : volt (unless refractory)
'''

P = NeuronGroup(10, eqs, threshold='v>Vt', reset='v = Vr',
                refractory=5*ms, method='euler')

#Monitor spikes
s_mon = SpikeMonitor(P)

#Monitor membrane potential
v_mon = StateMonitor(P, variables='v', record = [0])

run(.5 * second)

figure(figsize=(6,4))
plot(s_mon.t/ms, s_mon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
tight_layout()
ylim([-1, len(P)+1])
savefig('img/brian2_lif_raster.png')

figure(figsize=(6,4))
plot(v_mon.t/ms, v_mon.v[0], 'k')
xlabel('Time (ms)')
ylabel('Membrane potential [V]')
tight_layout()
savefig('img/brian2_lif_v.png')

show()
