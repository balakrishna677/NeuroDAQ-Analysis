""" Utility functions for IPython console
"""

import numpy as np
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from widgets import h5Item
from util import pgplot
from analysis import auxfuncs as aux


# Get browser instance
global browser

def set_browser(b):
    # Called by mainWindow.py to set global browser
    global browser
    browser = b


# Data functions
def get_data():
    """ Return the data currently plotted.
    """
    data = []
    for item in browser.ui.dataPlotsWidget.plotDataItems:
        #data.append(browser.ui.workingDataTree.data[item.dataIndex])
        data.append(item.data)
    data = np.array(data) # this will return an error if dts are different (data is not the same len)
    attrs = item.attrs
    
    if data.shape[0]==1:
        return data.ravel()
    else:    
        return data
            
def get_items():
    items = []
    for item in browser.ui.dataPlotsWidget.plotDataItems:       
        items.append(item)
    return items

def store_data(data, name='data', attrs={'dt':1}):
    """ Adds data to the Data Tree

    'data' is a number array of 1 or 2 dimensions
    'name' is sring
    'attrs' is a dictionary {attr1: value1, attr2, value2, ...}
    """
    # Set root as parent
    parentWidget = browser.ui.workingDataTree.invisibleRootItem()

    # Make sure data is numpy array
    data = np.array(data)

    # 1D array - add straight to root with name 'name' 
    if len(data.shape)==1:
        item = h5Item([name])
        browser.make_nameUnique(parentWidget, item, item.text(0))    
        item.data = data
        item.attrs = attrs
        item.listIndex = len(browser.ui.workingDataTree.dataItems)
        browser.ui.workingDataTree.dataItems.append(item)
        browser.ui.workingDataTree.addTopLevelItem(item)

    # 2D array - add 'name' group and 'data' datasets
    elif len(data.shape)==2:
        item = h5Item([name])
        browser.make_nameUnique(parentWidget, item, item.text(0)) 
        browser.ui.workingDataTree.addTopLevelItem(item)
        for n in np.arange(0, len(data)):
            child = h5Item(['data_'+str(n)])
            browser.make_nameUnique(item, child, child.text(0))
            child.data = data[n,:]
            child.attrs = attrs
            child.listIndex = len(browser.ui.workingDataTree.dataItems)
            browser.ui.workingDataTree.dataItems.append(child)
            item.addChild(child)

            
# Ploting functions
def plot_data(data, clear=False):
    """ Plot a single trace.
    
    Set clear = True to clear plot
    """
    plotWidget = browser.ui.dataPlotsWidget
    if clear: plotWidget.clear()
    plotWidget.plot(data, pen=pg.mkPen('#3790CC'))

def get_cursors(X=False):
    """ Returns the position of the 2 vertical cursors
    in the data plot tab. 

    c1, c2 = get_cursors()

    Default is to return in position in sampling points,
    set X=True to return positions in X-axis coordinates.
    """
    plotWidget = browser.ui.dataPlotsWidget
    c1 = plotWidget.cursor1.value()
    c2 = plotWidget.cursor2.value() 
    if c2<c1:        
        temp = c2
        c2 = c1
        c1 = temp
    dt = aux.get_attr(plotWidget.plotDataItems, 'dt')[0]  # Assumes dt is the same for all plotted items
    if X:
        return int(c1), int(c2)
    else:
        return int(c1/dt), int(c2/dt)






 





