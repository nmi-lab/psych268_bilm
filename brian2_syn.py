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

Cm = 50*pF; gl = 1e-9*siemens; taus = 5*ms
Vt = -50*mV; Vr = -60*mV; El = -60*mV

eqs = '''
dv/dt  = -gl*(v-El)/Cm + .1*xi/sqrt(ms)*mV+isyn/Cm : volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
'''

Pin = PoissonGroup(10, rates = 50*Hz)
P = NeuronGroup(10, eqs, threshold='v>Vt', reset='v = Vr',
                refractory=5*ms, method='euler')

w = .1 * nA
S = Synapses(Pin, P, on_pre='isyn += w')
S.connect('i==j')

s_mon = SpikeMonitor(P)

v_mon = StateMonitor(P, variables='v', record = [0])
isyn_mon = StateMonitor(P, variables='isyn', record = [0])

run(.5 * second)

figure(figsize=(6,4))
plot(s_mon.t/ms, s_mon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
ylim([-1,len(P)+1])
tight_layout()
savefig('img/brian2_syn_raster.png')

figure(figsize=(6,4))
ax = axes()
ax2 = ax.twinx()
ax.plot(v_mon.t/ms, v_mon.v[0]/mV, 'k')
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Membrane potential [mV]')
ax2.plot(isyn_mon.t/ms, isyn_mon.isyn[0]/nA, 'b', linewidth = 3, alpha=.4)
ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Synaptic Current [nA]')
tight_layout()
savefig('img/brian2_syn_i.png')
show()
