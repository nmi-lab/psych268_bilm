#!/bin/python
#-----------------------------------------------------------------------------
# File Name : 
# Author: Emre Neftci
#
# Creation Date : Thu 13 Oct 2016 04:22:48 PM PDT
# Last Modified : 
#
# Copyright : (c) UC Regents, Emre Neftci
# Licence : GPLv2
#----------------------------------------------------------------------------- 
#Spike-timing dependent plasticity, adapted from Brian2 Website
from brian2 import *
#Neuron parameters
Cm = 50*pF; gl = 1e-9*siemens; taus = 5*ms
sigma = 3/sqrt(ms)*mV; Vt = 10*mV; Vr = 0*mV;  
#STDP Parameters
taupre = 20*ms; taupost = taupre
apre = .01e-12; apost = -apre * taupre / taupost * 1.05

eqs = '''
dv/dt  = -gl*v/Cm + isyn/Cm + sigma*xi: volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
'''

Pin = PoissonGroup(10, rates = 30*Hz)
P = NeuronGroup(1, eqs, threshold='v>Vt', reset='v = Vr',
                      method='euler', refractory=5*ms)
S = Synapses(Pin, P, '''w : 1
                        dx/dt = -x / taupre  : 1
                        dy/dt = -y / taupost : 1''',
             on_pre='''isyn += w*amp
                        x += apre
                        w += y''',
             on_post='''y += apost
                        w += x''')

S.connect()
S.w = '(rand()-.5)*1e-9'
mon = StateMonitor(S, variables=['w','x','y'], record=range(5))
s_mon = SpikeMonitor(P)
p_mon = SpikeMonitor(Pin)

run(1*second, report='text')

figure(figsize=(6,4))
subplot(211)
for i in p_mon.t[p_mon.i==0]/ms:
    axvline(i, color='b')
for i in s_mon.t[s_mon.i==0]/ms:
    axvline(i, color='r')
plot(mon.t/ms, mon.x[0], 'b', linewidth=3, alpha=.6)
plot(mon.t/ms, mon.y[0], 'r', linewidth=3, alpha=.6)
subplot(212)
for i in p_mon.t[p_mon.i==0]/ms:
    axvline(i, color='b')
for i in s_mon.t[s_mon.i==0]/ms:
    axvline(i, color='r')
plot(mon.t/ms, mon.w[0], 'k', linewidth=3, alpha=.6)
xlabel('Time (s)')
ylabel('Weight')
tight_layout()
savefig('img/brian2_stdp_deltaw.png')

show()



