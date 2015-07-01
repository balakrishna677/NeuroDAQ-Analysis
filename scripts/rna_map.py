import numpy as np
import matplotlib.pylab as plt
from analysis import smooth
from console import utils as ndaq
import matplotlib as mpl
import matplotlib.gridspec as gridspec

# Display RNA seq data a colormap

# Get data
data = np.array([4.34,7.19,6.99,0,1.04,3.45,3.98,6.82,0,1.23])

# Make into matrix
data = np.repeat(data, 10)
data.shape = (10, 10)

# Define max value for normalization
vmax = 7.17*1.5

# Colormap
cmap = plt.cm.gist_heat

# Remove all existing axes
for ax in canvas.fig.axes:
    canvas.fig.delaxes(ax)
       
# Create grid
nPlots, width_ratios = 2, [10,1]
gs = gridspec.GridSpec(1, nPlots, width_ratios=width_ratios)

# Create subplots
ax = []
for plot in range(nPlots):
    ax.append(canvas.fig.add_subplot(gs[plot]))

# Show matrix
#ax[0].axis('off')
#ax.linewidth=50.0
ax[0].matshow(data, cmap=cmap, vmin=0, vmax=vmax, interpolation='none',aspect='auto')
norm = mpl.colors.Normalize(vmin=0, vmax=vmax)    

# Show colorbar
cbar = mpl.colorbar.ColorbarBase(ax[1], cmap=cmap, norm=norm, spacing='proportional')
cbar.set_label('cm/s', rotation=0, labelpad=10, y=1)
cbar.set_ticklabels(['Low', 'Medium'])# horizontal colorbar
mpl.rcParams.update({'font.size': 14})

canvas.draw()

