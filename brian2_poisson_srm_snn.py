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

from brian2 import *

Cm = 50*pF; gl = 1e-9*siemens; taus = 5*ms
Vr = 0*mV; El = 0*mV

eqs = '''
dv/dt  = -gl*(v-El)/Cm + isyn/Cm + iext/Cm: volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
iext : amp
'''

Pin = PoissonGroup(10, rates = 50*Hz)
P = NeuronGroup(100, eqs, reset='v = v',refractory=0*ms, method='euler',
                threshold='rand()<(1-exp(-exp(v/volt)*dt/second))')

wff = 2.0 * nA
Sff = Synapses(Pin, P, on_pre='isyn += wff')
Sff.connect('i==j')

wrec = -.01 * nA
Srec = Synapses(P, P, on_pre='isyn += wrec')
Srec.connect()

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
savefig('img/brian2_snn_raster.png')

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
savefig('img/brian2_snn_i.png')

show()
