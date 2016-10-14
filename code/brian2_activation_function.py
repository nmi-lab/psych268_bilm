#!/bin/python
#-----------------------------------------------------------------------------
# File Name : brian2_lif.py
# Author: Emre Neftci
#
# Creation Date : Wed 28 Sep 2016 12:05:29 PM PDT
# Last Modified : Thu 06 Oct 2016 11:26:34 PM PDT
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

Cm = 50*pF; gl = 1e-9*siemens; taus = 20*ms
Vt = 10*mV; Vr = 0*mV;
sigma = 0./sqrt(ms)*mV
eqs = '''
dv/dt  = - gl*v/Cm 
         + sigma*xi
         + iext/Cm : volt (unless refractory)
iext : amp
'''

P = NeuronGroup(100, eqs, threshold='v>Vt', reset='v = Vr',
                refractory=0*ms, method='milstein')

P.v = Vr #Set initial V to reset voltage
P.iext = np.linspace(-.2, .8, 100)*.1*nA

s_mon = SpikeMonitor(P)

run(5.0 * second)

#Plotting
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
