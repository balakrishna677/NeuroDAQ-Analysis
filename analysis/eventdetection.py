""" Event detection functions
"""

import numpy as np
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from widgets import h5Item
from util import pgplot
import auxfuncs as aux

def event_detect(browser):
    """ Temporary event detection function using amplitude
    threshold only. Noise safety is for when coming down from
    peak, go down an extra amount from threshold before starting
    to search for the next event.
    """
    # Read detection options
    threshold = float(browser.ui.toolStackedWidget.eventThreshold.text())
    noiseSafety = float(browser.ui.toolStackedWidget.eventNoiseSafety.text())

    # Get data currently plotted and concatenate in a single sweep
    data = aux.get_data(browser)
    data = data.ravel()

    # Run detection   
    comp = lambda a, b: a < b
    eventCounter,i = 0,0
    xOnsets, yOnsets = [], []
    while i<len(data):
        if comp(data[i],threshold):
            xOnsets.append(i)
            yOnsets.append(data[i])
            eventCounter +=1
            while i<len(data) and comp(data[i],(threshold-noiseSafety)):
                i+=1 # skip values if index in bounds AND until the value is below/above threshold again
        else:
            i+=1
    print eventCounter, 'events detected'

    # Store event onsets and peaks
    print data.shape
    item = h5Item(['Events'])
    browser.ui.workingDataTree.addTopLevelItem(item)
    store_array(browser, item, 'trace', np.array(data))
    store_array(browser, item, 'onsets', np.array(xOnsets))
    store_array(browser, item, 'peaks', np.array(yOnsets))
    
    # Plot results
    plot_events(browser, data, np.array(xOnsets), np.array(yOnsets))
    #return eventCounter, np.array(xOnsets), np.array(yOnsets)



def store_array(browser, parent, childName, array):
    child = h5Item([childName]) 
    parent.addChild(child)
    child.dataIndex = len(browser.ui.workingDataTree.data) 
    browser.ui.workingDataTree.data.append(array)


def plot_events(browser, data, xOnsets, yOnsets):
    plotWidget = browser.ui.dataPlotsWidget
    plotWidget.clear()
    plotWidget.plot(data)
    for e in np.arange(0, len(xOnsets)):
        plotWidget.plot([xOnsets[e]], [yOnsets[e]], pen=None, symbol='o', symbolPen='r', symbolBrush=None, symbolSize=7)


