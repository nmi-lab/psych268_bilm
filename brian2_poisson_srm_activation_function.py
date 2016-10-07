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
def mean_rates(s_mon):
    rates = np.zeros(np.max(s_mon.i)+1)
    for k,v in s_mon.spike_trains().iteritems():
        rates[k] = len(v)
    return rates/s_mon.t[-1]

from brian2 import *

Cm = 50*pF; gl = 1e-9*siemens; taus = 5*ms
Vr = 0*mV; El = 0*mV

eqs = '''
dv/dt  = - gl/Cm*v
         + (isyn+iext)/Cm : volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
iext : amp
'''

#Poisson Neuron
P = NeuronGroup(100, eqs, reset='v = v',refractory=0*ms, method='euler',
                threshold='rand()<(1-exp(-exp(v/volt)*dt/second))')
                
P.v = Vr
P.iext = np.linspace(-20, 80, len(P))*.1*nA

s_mon = SpikeMonitor(P)

run(5.0 * second)

figure(figsize=(6,4))
plot(s_mon.t/ms, s_mon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
ylim([-1,len(P)+1])
xlim(0,1000)
tight_layout()
savefig('img/brian2_activation_function_raster.png')

figure(figsize=(6,4))
plot(P.iext/nA, mean_rates(s_mon), 'b-', linewidth=3, alpha=.6)
xlabel('Iext [nA]')
ylabel('Firing Rate [Hz]')
tight_layout()
savefig('img/brian2_activation_function.png')
show()
