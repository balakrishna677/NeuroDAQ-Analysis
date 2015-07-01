# Sort events in current pulse trains
# 
# Select item with pulse trains to start

import numpy as np
import matplotlib.pylab as plt
from console import utils as ndaq

# Get data
item =  browser.ui.workingDataTree.selectedItems()[0]

# Iterate events and get traces
data, onsets = [], []
for c in range(item.childCount()):
    data.append(item.child(c).data)

# Get dt
dt = item.child(1).attrs['dt']

# Get events
pstart = int(500./dt)
pnumber = 20
ebsl = int(5./dt)
edur = int(100./dt)
isi = int(200./dt)
events = []
estarts = np.arange(pstart, pstart+isi*pnumber, isi)
for trace in data:
    for t in estarts:
        events.append(trace[t-ebsl:t+ebsl+edur])


# Sort by baseline Vm
def vm_sort(limits): 
    # imits is tuple with (vmin, vmax)
    dataSort = []
    for e in events:
        vm = np.mean(e[0:ebsl])
        if vm>limits[0] and vm<limits[1]:
            dataSort.append(e)            
    dataSort = np.array(dataSort)
    #plt.plot(dataSort.mean(axis=0))
    return dataSort

# Baseline and average without plotting
def avg(data):
    mData = np.mean(data, axis=0)
    return mData    

def baseline(data):
    data = np.array(data)
    for n in range(len(data)):
        b = np.mean(data[n][0:ebsl])
        data[n] = data[n]- b
    return data    

# Get rid of negative/positive going events
def neg(data, limit):
    # limit is fraction of min or max
    dataClean, dataNorm = [], []
    for n in data:
        epeak = n[0:10/0.02].max()
        if n.min()>-limit[0]*epeak and n.max()<limit[1]*epeak: 
            dataClean.append(n)
            dataNorm.append(n/epeak)
    return dataClean, dataNorm

# Run
#result = vm_sort((-50,-10))
result = vm_sort((-75,-15))
#result = isi_sort(100)
result = baseline(result)
result1, result2 = neg(result, (0.5,1.5))
#result = avg(result)


# Save
#ndaq.store_data(events, name='events', attrs={'dt':dt})
#ndaq.store_data(result, name='events', attrs={'dt':dt})
#ndaq.store_data(result1, name='events_clean', attrs={'dt':dt})
ndaq.store_data(result2, name='events_norm', attrs={'dt':dt})
