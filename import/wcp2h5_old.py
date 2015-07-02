import os
import numpy as np
import scipy.io
import h5py


def wcp2h5(folder, overwrite=False):
    """ Convert .WCP files to .hdf5.
    
    Works with 1 or 2 channels.
    """

    # List of all files in folder to skip conversion if needed
    h5fileList = os.listdir(folder)

    # Iterate through files
    for fname in os.listdir(folder):
        ext = os.path.splitext(fname)[1]    
        if ext=='.wcp':
            h5fname = fname.rstrip(ext) + '.hdf5'  

            # Skip previoulsy converted files
            if not overwrite:
                if (h5fname in h5fileList)==True:
                    print 'skipped file', h5fname          

            # Open WCP file                  
            else:
                fwcp = open(folder+'/'+fname, 'rb')
                
                # Read HEADER block
                nLinesHeader = 26
                hList = []
                for l in np.arange(0, nLinesHeader):
                    hList.append(fwcp.readline())
               
                #for l in np.arange(0, len(hList)):
                #    print l, hList[l]
                ADCMAX = int(hList[3].strip('ADCMAX=\r\n'))
                NC = int(hList[4].strip('NC=\r\n'))
                NBA = int(hList[5].strip('NBA=\r\n'))  
                NBD = int(hList[6].strip('NBD=\r\n'))
                NR = int(hList[8].strip('NR=\r\n'))
                DT = float(hList[9].strip('DT=\r\n'))
                YU0 = hList[12].strip('YUO=\r\u')
                YG0 = float(hList[14].strip('YG0=\r\n'))
                if NC==2:
                    YU1 = hList[19].strip('YU1=\r\u')
                    YG1 = float(hList[20].strip('YG1=\r\n'))                    

                # Read ANALYSIS block
                fwcp.seek(1024,0)
                aBlock = fwcp.read(NBA*512)
                VMAX = np.fromstring(aBlock[24:28], dtype=np.float32)

                # Read DATA block
                dList = []
                for rec in np.arange(0, NR):
                    recStart = 1024 + rec*(NBA*512 + NBD*512) + 1024
                    fwcp.seek(recStart,0)
                    recData = np.fromstring(fwcp.read(NBD*512), dtype=np.int16)
                    if NC==2:
                        chn1 = recData[0::2]
                        chn1 = VMAX/(ADCMAX*YG0)*chn1
                        chn2 = recData[1::2]
                        chn2 = VMAX/(ADCMAX*YG1)*chn2
                        dList.append([chn1, chn2])
                    else:
                        recData = VMAX/(ADCMAX*YG0)*recData
                        dList.append(recData)
                data = np.array(dList)
                print data.shape

                # Open HDF5 file
                print folder+'/'+h5fname
                f = h5py.File(folder+'/'+h5fname, 'w')             
             
                # Iterate through records and add to root
                if NC==2:
                    g1 = f.create_group('Channel_1')
                    g2 = f.create_group('Channel_2')
                    for rec in np.arange(0, len(data)):
                        dset1 = g1.create_dataset('data_'+str(rec), data=data[rec,0,:])    
                        dset2 = g2.create_dataset('data_'+str(rec), data=data[rec,1,:])
                        
                        # Add some attributes
                        dset1.attrs['dt'] = DT
                        dset1.attrs['Raw_data_file'] = h5fname
                        dset2.attrs['dt'] = DT
                        dset2.attrs['Raw_data_file'] = h5fname                        
                else:
                    for rec in np.arange(0, len(data)):           
                        dset = f.create_dataset('/data_'+str(rec), data=data[rec,:])
                         
                        # Add some attributes
                        dset.attrs['dt'] = DT
                        dset.attrs['Raw_data_file'] = h5fname         
                                
                # Close HDF5 file
                print 'Converted', fname
                f.close()                
                        


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def batch_convert(folder, overwrite=False):
    """ Recursively convert all files in all folders from a
    starting folder
    """        
    # Convert files in the current folder
    wcp2h5(folder, overwrite=overwrite)
    
    # Recurse through folders
    for folder in listdir_fullpath(folder):
        print 'Converting files in folder', folder    
        if os.path.isdir(folder):
            batch_convert(folder, overwrite=overwrite)

