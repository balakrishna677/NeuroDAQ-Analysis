import numpy as np
import matplotlib.pylab as plt
from console import utils as ndaq

# Get data
data = ndaq.get_data()

# Subtract average of all channels from each channel
# baseline traces first
avg = data.mean(axis=0)
refData = []
for n in range(len(data)):
    refData.append(data[n,:]-avg)

# Store data
ndaq.store_data(refData, name='refData', attrs={'dt': 1./30})


