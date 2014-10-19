import numpy as np
import scipy.signal as signal
from analysis import smooth
from console import utils as ndaq

def fft_spectrum(data, Fs):
    """ Calculate the single-sided amplitude spectrum
    of data sampled at Fs frequency.
    """
    
    n = len(data)    # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T     # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
    Y = np.fft.fft(data)/n # fft computing and normalization
    Y = Y[range(n/2)]
    return frq, np.abs(Y)

def applyFilter(data, b, a, padding=100, bidir=True):
    """Apply a linear filter with coefficients a, b. Optionally pad the data before filtering
    and/or run the filter in both directions."""
    try:
        import scipy.signal
    except ImportError:
        raise Exception("applyFilter() requires the package scipy.signal.")
    
    d1 = data.view(np.ndarray)
    
    if padding > 0:
        d1 = np.hstack([d1[:padding], d1, d1[-padding:]])
    
    if bidir:
        d1 = scipy.signal.lfilter(b, a, scipy.signal.lfilter(b, a, d1)[::-1])[::-1]
    else:
        d1 = scipy.signal.lfilter(b, a, d1)
    
    if padding > 0:
        d1 = d1[padding:-padding]
        
    if (hasattr(data, 'implements') and data.implements('MetaArray')):
        return MetaArray(d1, info=data.infoCopy())
    else:
        return d1
        
def besselFilter(data, cutoff, order=1, dt=None, btype='low', bidir=True):
    """return data passed through bessel filter"""
    try:
        import scipy.signal
    except ImportError:
        raise Exception("besselFilter() requires the package scipy.signal.")
    
    if dt is None:
        try:
            tvals = data.xvals('Time')
            dt = (tvals[-1]-tvals[0]) / (len(tvals)-1)
        except:
            dt = 1.0
    
    b,a = scipy.signal.bessel(order, cutoff * dt, btype=btype) 
    
    return applyFilter(data, b, a, bidir=bidir)


def removePeriodic(data, f0=50.0, dt=None, harmonics=10, samples=4):
    
    ft = np.fft.fft(data)
    
    ## determine frequencies in fft data
    df = 1.0 / (len(data) * dt)
    freqs = np.linspace(0.0, (len(ft)-1) * df, len(ft))
    
    ## flatten spikes at f0 and harmonics
    for i in xrange(1, harmonics + 2):
        f = f0 * i # target frequency
        
        ## determine index range to check for this frequency
        ind1 = int(np.floor(f / df)) - (samples/2)
        ind2 = int(np.ceil(f / df)) + (samples/2-1)
        if ind1 > len(ft)/2.:
            print f, 'breaking'
            break
        mag = (abs(ft[ind1-1]) + abs(ft[ind2+1])) * 0.5
        mag = mag * 0.1
        for j in range(ind1, ind2+1):
            phase = np.angle(ft[j])   ## Must preserve the phase of each point, otherwise any transients in the trace might lead to large artifacts.
            re = mag * np.cos(phase)
            im = mag * np.sin(phase)
            ft[j] = re + im*1j
            ft[len(ft)-j] = re - im*1j
            
    data2 = np.fft.ifft(ft).real
    return data2


def denoise(data, f0=50.0, dt=None, harmonics=10):
    ft = np.fft.rfft(data)
    
    ## determine frequencies in fft data
    df = 1.0 / (len(data) * dt)
    freqs = np.linspace(0.0, (len(ft)-1) * df, len(ft))
    
    # flatten spikes at f0 and harmonics
    f = f0  # target frequency
    mag = 0
    idx = f/df
    print f, df, idx, freqs[idx]
    ft[idx-100:idx+100] = mag
    out = np.fft.irfft(ft)         
    return out            

# Get data and items
data = ndaq.get_data()
items = ndaq.get_items()
dt = items[0].attrs['dt']
    
# FFT power spectrum
#frq, fData = fft_spectrum(data, 1/dt*1000)
#fdt = np.diff(frq)[0]
fData = besselFilter(data, 2000., 1, dt/1000.)
fData = removePeriodic(fData, 50.0, dt/1000., 20, 400)
#fData = removePeriodic(fData, 429.5, dt/1000., 20, 400)

#fData = denoise(data, 50.0, dt/1000.)

# Plot
#ndaq.plot_data(freqs, abs(ft), clear=True)

# Store
ndaq.store_data(fData, attrs={'dt':dt})
