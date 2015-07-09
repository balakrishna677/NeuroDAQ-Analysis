import numpy as np
import h5py
from nptdms import TdmsFile
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import neo
import quantities as pq
from OpenElectrophy.timefrequency import TimeFreq
from OpenElectrophy import neo_to_oe, open_db

###########
# Load Data
###########
# Get data from .nex files

filedir = '/home/tiago/Data/Lab.local/PAG/probe/'
fname = 'SE-CSC-RAW-Ch11_.nex'
r = neo.io.NeuroExplorerIO(filename=(filedir + fname)) 
seg = r.read_segment(lazy=False, cascade=True)
data = np.array(seg.analogsignals[0])

filedir = '/home/tiago/Data/Lab.local/PAG/probe/'
fname = 'Analog Input Ch16_.nex'
f = neo.io.NeuroExplorerIO(filename=(filedir + fname)) 
fseg = f.read_segment(lazy=False, cascade=True)
frames = np.array(fseg.analogsignals[0])

# Get tdms file corresponding to the recording
filedir = '/home/tiago/Data/Lab.local/PAG/probe/'
fname = '02-07-2015-19-48-64207_VG2_SC_probe_t1.tdms'
tdms = TdmsFile(filedir+fname)


#############
# Pre-process
#############
# Get rid of probe starting artefact
i = frames<(-1000)
counter = np.arange(0,len(i))
dataStart = counter[i][-1]+100
frames = frames[dataStart:]

# Get the start of each frame
dframes = np.diff(frames)
counter = np.arange(0,len(dframes))
i = dframes>1000
frameIndex = counter[i]
dataFrameStart = frameIndex[0]
print len(frameIndex), 'frames detected'

#######################
# Cut times of interest
#######################
onset = 26900 #30000 #26900
pre = 200
post = 800
start = onset-pre
end = onset+post

# Cut tdms
pos = tdms.object('Real-time Coordinates', 'X-Vertical').data[start:end]
spot = tdms.object('Visual  Stimulation', 'Spot Diameter').data[start:end]

# Cut probe data
#print frameIndex[onset]
pstart = frameIndex[start]+dataStart
pend = frameIndex[end]+dataStart
trace = data[pstart:pend]
#print len(data)
#print pstart, pend, len(trace)

###############
# Make neo file
###############
#bl = neo.Block(name='Ch2')
#seg = neo.Segment(name='Trial_1')
#bl.segments.append(seg)
anasig = neo.AnalogSignal(trace, units='V', t_start=0*pq.s, sampling_rate=30000*pq.Hz)
#seg.analogsignals.append(anasig)
#savename = 'test.h5'
#s = neo.io.NeoHdf5IO(filename=filedir+savename)
#s.save(bl)
#s.close()

# Convert to OpenEphys
#open_db( url = 'sqlite:////home/tiago/Data/Lab.local/PAG/probe/test.sqlite', myglobals=globals(), use_global_session=True)
#oe_bl = neo_to_oe(bl, cascade=True)



##########################
# Caclulate time frequency
##########################
f_start = 1.
f_stop = 50.
deltafreq = (f_stop-f_start)/60.
tfr = TimeFreq(anasig, f_start=f_start, f_stop=f_stop, deltafreq=deltafreq, f0=2.5,  sampling_rate=f_stop*2.)
#print tfr.freqs
#print tfr.times
#print tfr.map.shape, tfr.map.dtype

###########
# Plot data
###########
# Remove all existing axes
for ax in canvas.fig.axes:
    canvas.fig.delaxes(ax)
       
# Create grid
nPlots, height_ratios = 3, [1,1]
gs = gridspec.GridSpec(nPlots, 1) #, height_ratios=height_ratios)

# Create subplots
ax = []
for plot in range(nPlots):
    ax.append(canvas.fig.add_subplot(gs[plot]))

ax[0].plot(spot)
ax[1].plot(pos)
tfr.plot(ax[2], colorbar=False, clim=[0,80])
canvas.draw()


############
# Store data
############








