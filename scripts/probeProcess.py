import numpy as np
import h5py
from nptdms import TdmsFile
import matplotlib.pylab as plt
from console import utils as ndaq

###########
# Load Data
###########
# Get probe data converted straight from .nex file
# in hdf5 format using nex2h5.py
# Last channel is analog input with frame starts (#14)
filedir = '/home/tiago/Data/isilon-science/PAG_project/raw_data/behaviour/2015/15JUL05_Probe/2015-07-05_20-39-14/'
#filedir = '/home/tiago/Data/Lab.local/PAG/probe/'
fname = filedir + 'rawdata.hdf5'
probe = h5py.File(fname, 'r+')
channels = probe['/channels']  #channel order is screwed up because of 1 instead of 01
#data = [channels[chn][:] for chn in channels]  # takes too long, change to read on request
frames = channels['channel_15'][:]

# Get tdms file corresponding to the recording
filedir = '/home/tiago/Data/isilon-science/PAG_project/raw_data/behaviour/2015/15JUL05_Probe/'
#filedir = '/home/tiago/Data/Lab.local/PAG/probe/'
fname = '05-07-2015-20-39-expanding white spot test.tdms'
tdms = TdmsFile(filedir+fname)

#############
# Pre-process
#############
# Get rid of probe starting artefact
#plt.plot(frames)
i = frames<(-1000)
counter = np.arange(0,len(i))
dataStart = counter[i][-1]+100
frames = frames[dataStart:]

# Get the start of each frame
dframes = np.diff(frames)
counter = np.arange(0,len(dframes))
i = dframes>5000
frameIndex = counter[i]
dataFrameStart = frameIndex[0]
print len(frameIndex), 'frames detected'

#######################
# Cut times of interest
#######################
onset = 0 #30000 #26900
pre = 800
post = 800
start = 0 #onset-pre
end = 3800 #onset+post

# Cut tdms
pos = tdms.object('Real-time Coordinates', 'X-Vertical').data[start:end]*10
spot = tdms.object('Visual  Stimulation', 'Spot Diameter').data[start:end]*10

# Cut probe data
#print frameIndex[onset]
data = []
print frameIndex[end], dataStart
pstart = frameIndex[start]+dataStart
pend = frameIndex[end]+dataStart
c = 0
for chn in channels:
    print chn
    trace = channels[chn][pstart:pend]
    data.append(trace-np.mean(trace)+c)
    c-=1000


###########
# Plot data
###########



############
# Store data
############
ndaq.store_data(pos, name='position', attrs={'dt':1./50})
ndaq.store_data(spot, name='spot', attrs={'dt':1./50})
ndaq.store_data(data, name='probe data', attrs={'dt':1./30000})
















