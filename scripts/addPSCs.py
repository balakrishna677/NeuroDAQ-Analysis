import numpy as np
import matplotlib.pylab as plt
import scipy.signal as signal
from analysis import smooth
from console import utils as ndaq

# Add single PSCs at a defined frequency and number

# Get data and items
data = ndaq.get_data()
items = ndaq.get_items()
dt = items[0].attrs['dt']
dt = 0.04

# Lag traces and add them
number = 20
freq = 20.
isi = 1/freq*1000 # in ms

result = []
for n in range(number):
    trace = data
    npad = int(n*isi/dt)
    laggedTrace = np.pad(trace, (npad, 0), 'constant', constant_values=(0,0)) 
    #if n>0: laggedTrace = laggedTrace[:-npad]
    result.append(laggedTrace)

maxshape = result[len(result)-1].shape
alignedTraces = []
c=0
for trace in result:
    size = len(trace)
    trace = np.resize(trace, maxshape)
    trace[size::] = 0
    alignedTraces.append(trace)
    #if c==1: plt.plot(trace)    
    c=c+1

summedTrace = np.array(alignedTraces).sum(axis=0)
plt.plot(summedTrace)
plt.show()

ndaq.store_data(summedTrace, attrs={'dt':1})

