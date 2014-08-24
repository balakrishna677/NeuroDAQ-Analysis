""" Functions for plotting using PyQtGraph
"""

import numpy as np
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

def plot_singleData(browser, plotWidget, data):
    plotWidget.clear()
    plotWidget.plot(data)

    
def plot_multipleData(browser, plotWidget):
    dt = 0.04
    plotWidget.clear()
    plotWidget.plotDataIndex = []
    plotWidget.xBoundaries = []
    plotWidget.yBoundaries = []    
    items = browser.ui.workingDataTree.selectedItems()
    if items:
        for item in items:
            if item.dataIndex is not None:
                x = np.arange(0, len(browser.ui.workingDataTree.data[item.dataIndex])*dt, dt)
                y = browser.ui.workingDataTree.data[item.dataIndex]
                plotWidget.plot(x, y)
                plotWidget.plotDataIndex.append(item.dataIndex)
                plotWidget.xBoundaries.append(x.max())
                plotWidget.yBoundaries.append([y.min(), y.max()])

def zoom_out(browser, plotWidget):
    if plotWidget.xBoundaries:
        plotWidget.setXRange(0, np.max(plotWidget.xBoundaries))
        plotWidget.setYRange(np.min(plotWidget.yBoundaries), np.max(plotWidget.yBoundaries))
