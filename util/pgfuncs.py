""" Functions for plotting using PyQtGraph
"""

import numpy as np
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

def plot_singleData(browser, plotWidget, data):
    """ Plot a single trace.
    """
    plotWidget.clear()
    plotWidget.plot(data, pen=pg.mkPen('#3790CC'))

    
def plot_multipleData(browser, plotWidget):
    """ Plot user-selected traces from the working data tree.

    Store the data indexes of the plotted items for use in 
    data analyis functions.
    
    Store max and min of data and x-axis for zoom out function.
    """
    plotWidget.clear()
    plotWidget.plotDataIndex, plotWidget.plotDataItems = [], []
    items = browser.ui.workingDataTree.selectedItems()
    if items:
        for item in items:
            if item.dataIndex is not None:
                try:
                    dt = item.attrs['dt']
                except KeyError:
                    dt = 1
                #print 'dt is', dt
                x = np.arange(0, len(browser.ui.workingDataTree.data[item.dataIndex])*dt, dt)
                y = browser.ui.workingDataTree.data[item.dataIndex]
                plotWidget.plot(x, y, pen=pg.mkPen('#3790CC'))
                plotWidget.plotDataIndex.append(item.dataIndex)
                plotWidget.plotDataItems.append(item)  # This makes plotDataIndex redundant, change later

def browse_singleData(browser, plotWidget, currentItem):
    """ Plot single trace of currentItem.
    Different from plot_singleData just to have dt.
    """
    plotWidget.clear()
    if currentItem.dataIndex is not None:
        try:
            dt = currentItem.attrs['dt']
        except KeyError:
            dt = 1    
        x = np.arange(0, len(browser.ui.workingDataTree.data[currentItem.dataIndex])*dt, dt)
        y = browser.ui.workingDataTree.data[currentItem.dataIndex]
        plotWidget.plot(x, y, pen=pg.mkPen('#3790CC'))        

def replot(browser, plotWidget):
    """ Function to replot the data currently in the data plot tab.
    Useful for visualising the data after any analysis transformation.
    """
    plotWidget.clear()
    for item in plotWidget.plotDataItems:  
        try:
            dt = item.attrs['dt']
        except KeyError:
            dt = 1
        x = np.arange(0, len(browser.ui.workingDataTree.data[item.dataIndex])*dt, dt)
        y = browser.ui.workingDataTree.data[item.dataIndex]
        plotWidget.plot(x, y, pen=pg.mkPen('#3790CC'))
              

def zoom_out(browser, plotWidget):
    """ Zoom out to the X and Y data boundaries.
    """ 
    if plotWidget.xBoundaries:
        plotWidget.setXRange(0, np.max(plotWidget.xBoundaries))
        plotWidget.setYRange(np.min(plotWidget.yBoundaries), np.max(plotWidget.yBoundaries))

def show_cursors(browser, plotWidget):
    """ Show two cursors for use in data analysis.
    """
    axisRange = plotWidget.viewRange()
    x1, x2 = axisRange[0]
    y1, y2 = axisRange[1]
    plotWidget.cursor1Pos = x1+(x2-x1)/2.-(x2-x1)*0.2  # start cursors 20% from the midline 
    plotWidget.cursor2Pos = x1+(x2-x1)/2.+(x2-x1)*0.2 
    plotWidget.cursor1 = pg.InfiniteLine(pos=plotWidget.cursor1Pos, angle=90, movable=True,
                                         pen=pg.mkPen('#2AB825', width=2, style=QtCore.Qt.DotLine))
    plotWidget.cursor2 = pg.InfiniteLine(pos=plotWidget.cursor2Pos, angle=90, movable=True, 
                                         pen=pg.mkPen('#2AB825', width=2, style=QtCore.Qt.DotLine))    
    plotWidget.addItem(plotWidget.cursor1)
    plotWidget.addItem(plotWidget.cursor2)

def hide_cursors(browser, plotWidget):
    """ Remove the data cursors.
    """
    plotWidget.cursor1Pos = []   
    plotWidget.cursor2Pos = []   
    plotWidget.removeItem(plotWidget.cursor1)
    plotWidget.removeItem(plotWidget.cursor2)

def replot_cursors(browser, plotWidget):
    """ Replot the cursors in the current positions
    after the axis had been clear for some reason
    """
    plotWidget.cursor1 = pg.InfiniteLine(pos=plotWidget.cursor1Pos, angle=90, movable=True, 
                                         pen=pg.mkPen('#2AB825', width=2, style=QtCore.Qt.DotLine))
    plotWidget.cursor2 = pg.InfiniteLine(pos=plotWidget.cursor2Pos, angle=90, movable=True,
                                         pen=pg.mkPen('#2AB825', width=2, style=QtCore.Qt.DotLine))    
    plotWidget.addItem(plotWidget.cursor1)
    plotWidget.addItem(plotWidget.cursor2)     
