import os
import numpy as np
import scipy.io
import h5py


def ephus2h5(folder):
    """ Convert recordings from Ephus into .hdf5 files.
    
    Works with two different formats: .xsg and .fig
    Only reads data from one channel.
    """
    # Manually set sampling rate
    dt = 0.1
    
    # List of all files in folder to skip conversion if needed
    h5fileList = os.listdir(folder)
    
    # Iterate through files
    for fname in os.listdir(folder):
        ext = os.path.splitext(fname)[1]        
        if (ext=='.fig') | (ext=='.xsg'):
            h5fname = fname.rstrip(ext) + '.hdf5'            
            
            # Skip previoulsy converted files
            if (h5fname in h5fileList)==True:
                print 'skipped file', h5fname          

            # Load Ephus file                  
            else:
                #print folder + fname
                mat = scipy.io.loadmat(folder+'/'+fname)
                if ext=='.xsg':
                    data = mat['data'][0][0][0][0][0][0]                
                elif ext=='.fig':
                    data = np.array(mat['hgS_070000'][0][0][3][0][0][3][0][0][2][0][0]).item()[2][0]
                    #data = temp.item()[2][0]

                # Open HDF5 file
                f = h5py.File(folder+'/'+h5fname, 'w')             
             
                # Create Channel 1 group and add data
                f.create_group('Channel_1')
                f.create_dataset('/Channel_1/data', data=data)
                
                # Add some attributes
                f.attrs['dt'] = dt
                                
                # Close HDF5 file
                print 'Converted', fname
                f.close()


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def batchConvert(folder):
    """ Recursively convert all files in all folders from a
    starting folder
    """        
    # Convert files in the current folder
    ephus2h5(folder)
    
    # Recurse through folders
    for folder in listdir_fullpath(folder):
        print 'Converting files in folder', folder    
        if os.path.isdir(folder):
            batchConvert(folder)

