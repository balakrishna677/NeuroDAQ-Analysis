import numpy as np
import scipy.signal as signal
from analysis import smooth
from console import utils as ndaq
       
# Get data and items
data = ndaq.get_data()
items = ndaq.get_items()
dt = items[0].attrs['dt']

# Make average trace
avg = data.mean(0)
avgPeak = avg.min()
xpeak = np.argmin(avg)

# Clear plot
#ndaq.plot_data([0], clear=True)

# Go through events
results1, results2 = [], []
nbins = 30
for trace in data:
    # Scale average
    peak = trace.min()
    sf = peak/avgPeak
    scaledAvg = avg*sf

    # Get decay part only
    decay = trace[xpeak+25:]
    avgDecay = avg[xpeak+25:]

    # Divide into bins
    binSize = decay.min()/nbins    

    # Get mean and variance current per bin
    m, v = [], []
    for b in range(nbins):
        ymin = b*binSize
        ymax = (b+1)*binSize
        i = (decay<ymin) & (decay>ymax)  # For inward currents
        current = decay[i].mean()
        var = np.mean((decay[i]-avgDecay[i])**2)
        
        m.append(current)
        v.append(var)
    
    results1.append(np.array(m))
    results2.append(np.array(v)) 
    #ndaq.plot_data(np.array(m), np.array(v))

# Store
ndaq.store_data(results1)
ndaq.store_data(results2)

