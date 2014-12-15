""" Functions for dealing with images
"""

import numpy as np

def array2image(data, shape):
    """ Converts a 1D array of pixels into a 
    2D array with shape 'shape'. 
    
    'shape' is a tuple, eg: (512, 512)
    """
    
    image = np.reshape(data, shape)
    return image

