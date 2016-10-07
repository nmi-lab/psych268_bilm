#!/bin/python
#-----------------------------------------------------------------------------
# File Name : 
# Author: Emre Neftci
#
# Creation Date : Wed 28 Sep 2016 12:05:59 PM PDT
# Last Modified : 
#
# Copyright : (c) UC Regents, Emre Neftci
# Licence : GPLv2
#----------------------------------------------------------------------------- 

from brian2 import *

Cm = 50*pF; gl = 1e-9*siemens; taus = 3*ms
Vt = -50*mV; Vr = -60*mV; El = -60*mV

eqs = '''
dv/dt  = - gl*(v-El)/Cm 
         + .1*xi/sqrt(ms)*mV
         + (isyn+iext)/Cm : volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
iext : amp
'''

P = NeuronGroup(3, eqs, threshold='v>Vt', reset='v = Vr',
                refractory=5*ms, method='euler')
P[0:1].iext = .015 * nA
P[1:2].iext = .01 * nA
P[2:3].iext = -.014 * nA

wrec = .21 * nA
Srec = Synapses(P, P, on_pre='isyn += wrec')
Srec.connect(i=0,j=2)
Srec.connect(i=1,j=2)

s_mon = SpikeMonitor(P)
v_mon = StateMonitor(P, variables='v', record = [2])
isyn_mon = StateMonitor(P, variables='isyn', record = [2])

run(1.0 * second)

figure(figsize=(6,4))
plot(s_mon.t/ms, s_mon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
ylim([-1,len(P)+1])
tight_layout()
savefig('img/brian2_coincidence_raster.png')

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
savefig('img/brian2_coincidence_i.png')

show()
