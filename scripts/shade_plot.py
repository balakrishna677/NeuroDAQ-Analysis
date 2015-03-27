import numpy as np
import matplotlib.pylab as plt
from analysis import smooth
from console import utils as ndaq
import matplotlib as mpl
import matplotlib.gridspec as gridspec

# Plot mean and error as shade
# Data as [avg+sem, avg-sem, avg]

# Get data
data = ndaq.get_data()

# Put data into horizontal matrix
data = np.array(data)

# Remove all existing axes
for ax in canvas.fig.axes:
    canvas.fig.delaxes(ax)
       
# Create grid
nPlots, width_ratios = 1, [1]
gs = gridspec.GridSpec(1, nPlots, width_ratios=width_ratios)

# Create subplots
ax = []
for plot in range(nPlots):
    ax.append(canvas.fig.add_subplot(gs[plot])) 
       
# Plot
x = np.arange(0, len(data[0]))
ax[0].plot(x, data[0], 'k')
ax[0].fill_between(x, data[1], data[2])

canvas.draw()

