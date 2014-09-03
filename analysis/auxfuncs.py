""" Auxiliary analysis functions for 1D data
"""

import numpy as np
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from widgets import h5Item
from util import pgplot

def get_data(browser):
    """ Return the data currently plotted.
    """
    data = []
    for index in browser.ui.dataPlotsWidget.plotDataIndex:
        data.append(browser.ui.workingDataTree.data[index])
    data = np.array(data)
    return data

def get_cursors(plotWidget):
    """ Return the current position of the data cursors.
    """
    c1 = plotWidget.cursor1.value()
    c2 = plotWidget.cursor2.value()
    plotWidget.cursor1Pos = c1     # Store positions for re-plotting
    plotWidget.cursor2Pos = c2    
    if c2<c1:        
        temp = c2
        c2 = c1
        c1 = temp
    return int(c1/plotWidget.dt), int(c2/plotWidget.dt)

def make_data_copy(browser, plotWidget):
    """ Make a copy of the currently plotted data to work on, 
    in order to keep the original data intact. Add new items
    to the working data tree and plot them, so that plotDataIndex
    is updated.
    """
    plotWidget.clear()
    newPlotDataIndex = []
    data = get_data(browser)
    dataIndex = plotWidget.plotDataIndex   
    item = h5Item(['Baselined_traces'])
    browser.ui.workingDataTree.addTopLevelItem(item)     
    for t in range(len(data)):
        # Add items to tree
        child = h5Item([str(t)])
        item.addChild(child)
        child.dataIndex =  len(browser.ui.workingDataTree.data)
        browser.ui.workingDataTree.data.append(browser.ui.workingDataTree.data[dataIndex[t]])   
        # Plot data copy
        x = np.arange(0, len(browser.ui.workingDataTree.data[child.dataIndex])*plotWidget.dt, plotWidget.dt)
        y = browser.ui.workingDataTree.data[child.dataIndex]
        plotWidget.plot(x, y, pen=pg.mkPen('#3790CC'))
        newPlotDataIndex.append(child.dataIndex)
    plotWidget.plotDataIndex = newPlotDataIndex
    if browser.ui.actionShowCursors.isChecked(): pgplot.replot_cursors(browser, plotWidget) 

def plot_point(plotWidget, cursor1, xpoint, ypoint):
    """ Plots a single point, with the X coordinate measured from the position
    of cursor 1 (i.e.: cursor 1 x position = 0). Useful from when processing data
    within the cursor range and needing to plot the results on top of the entire trace.
    """
    x = (xpoint + cursor1) * plotWidget.dt
    plotWidget.plot([x], [ypoint], pen=None, symbol='o', symbolPen='r', symbolBrush=None, symbolSize=7)


