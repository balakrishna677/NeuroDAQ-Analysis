""" Basic analysis functions for 1D data
"""

import numpy as np
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from widgets import h5Item
from util import pgplot
import smooth
import auxfuncs as aux


def baseline(browser):
    """ Subtract a baseline from the currently plotted traces.
    Baseline is the average of all datapoints between the 
    current position of the data cursors. 
    
    Options:
    1) keep original traces intact and create processed copies
    """
    plotWidget = browser.ui.dataPlotsWidget
    toolsWidget = browser.ui.toolStackedWidget   
    c1, c2 = aux.get_cursors(plotWidget) 

    # Check selected options
    for option in toolsWidget.baselineToolOptions:
        if option.isChecked():
            if option.text()=='Keep original data':
                aux.make_data_copy(browser, plotWidget)

    # Get the data now, in case we are working on a copy
    plotWidget.clear()    
    data = aux.get_data(browser)
    dataIndex = plotWidget.plotDataIndex 
    
    # Get dt list
    dtList = aux.get_attr(plotWidget.plotDataItems, 'dt')
    dt = dtList[0]

    # Make average between cursors and subract for each trace 
    for item in plotWidget.plotDataItems:
        bsl = np.mean(item.data[c1/dt:c2/dt])
        item.data = item.data - bsl

    #for t in range(len(data)):
        #browser.ui.workingDataTree.data[dataIndex[t]] = data[t]-bsl
    #    bsl = np.mean(data[t][c1/dtList[t]:c2/dtList[t]])
    #    plotWidget.plotDataItems[dataIndex[t]] = data[t]-bsl

    # Re-plot data
    pgplot.replot(browser, plotWidget)
    pgplot.replot_cursors(browser, plotWidget)    

def average_traces(browser):
    """ Calculate average trace from currently plotted traces.

    Options:
    1) create new entry in Working Data tree with the result
    2) plot average with orginal traces
    """
    plotWidget = browser.ui.dataPlotsWidget
    toolsWidget = browser.ui.toolStackedWidget
    plotWidget.clear()
    data = aux.get_data(browser)   

    # Get dt list (at this stage they will all be the same 
    # because otherwise get_data would have thrown an error
    dtList = aux.get_attr(plotWidget.plotDataItems, 'dt')
    dt = dtList[0]

    avgData = np.mean(data,0)

    # Check selected options
    for option in toolsWidget.avgToolOptions:
        if option.isChecked():
            if option.text()=='Store result':
                item = h5Item(['Avg'])
                parentWidget = browser.ui.workingDataTree.invisibleRootItem()
                browser.make_nameUnique(parentWidget, item, item.text(0))
                browser.ui.workingDataTree.addTopLevelItem(item)
                item.dataIndex = len(browser.ui.workingDataTree.data)
                browser.ui.workingDataTree.data.append(avgData)
            
            if option.text()=='Show traces':
                pgplot.replot(browser, plotWidget)
        
    # Plot average
    x = np.arange(0, len(avgData)*dt, dt)
    plotWidget.plot(x, avgData, pen=pg.mkPen('#CF1C04', width=2))
    if browser.ui.actionShowCursors.isChecked(): pgplot.replot_cursors(browser, plotWidget)      

def measure_cursor_stats(browser):
    """ Measure selected properties or statistics in the region defined
    by the data cursors.
    
    Options:
    1) create new entries in Working Data tree with the results
    """
    plotWidget = browser.ui.dataPlotsWidget
    toolsWidget = browser.ui.toolStackedWidget
    data = aux.get_data(browser)  
    c1, c2 = aux.get_cursors(plotWidget) 
    dataIndex = plotWidget.plotDataIndex     
    saveData = False

    # Get dt list
    dtList = aux.get_attr(plotWidget.plotDataItems, 'dt')

    # Go through data and check selected values to measure
    # Can probably do this in a more efficient way
    results = []
    for option in toolsWidget.measureToolOptions:
        if option.isChecked():
            if option.text()=='Store result':
                saveData = True        

            if option.text()=='Minimum':
                dataMin = ['Minimum']
                for t in range(len(data)):
                    dt = dtList[t]
                    y = np.min(data[t][c1/dt:c2/dt])
                    #x = np.where(data[t][c1:c2]==y)
                    x = np.argmin(data[t][c1/dt:c2/dt])
                    dataMin.append(y)
                    aux.plot_point(plotWidget, c1/dt, x, y, dt)
                results.append(dataMin)        

            if option.text()=='Maximum':
                dataMax = ['Maximum']
                for t in range(len(data)):
                    dt = dtList[t]
                    y = np.max(data[t][c1/dt:c2/dt])
                    #x = np.where(data[t][c1:c2]==y)
                    x = np.argmax(data[t][c1/dt:c2/dt])
                    dataMax.append(y)
                    aux.plot_point(plotWidget, c1/dt, x, y, dt)
                results.append(dataMax)    

            if option.text()=='Mean':
                dataMean = ['Mean']
                for t in range(len(data)):
                    dt = dtList[t]
                    y = np.mean(data[t][c1/dt:c2/dt])
                    dataMean.append(y)
                    plotWidget.plot([c1,c2], [y,y], pen=pg.mkPen('#CF1C04', width=1))
                results.append(dataMean)

    # Store results
    if saveData: aux.save_results(browser, 'Measurements', results)
    

def smooth_traces(browser):
    """ Smooth traces
    
    Options:
    1) Window type
    2) Window length
    """
    
    # Get options
    window = str(browser.ui.toolStackedWidget.smoothComboBox.currentText())
    window_len = float(browser.ui.toolStackedWidget.smoothLength.text())
    
    # Get data and widgets
    plotWidget = browser.ui.dataPlotsWidget
    toolsWidget = browser.ui.toolStackedWidget
    data = aux.get_data(browser) 
    
    # Get dt
    dt = aux.get_attr(plotWidget.plotDataItems, 'dt')[0]
    
    # Smooth data
    results = [] 
    for t in range(len(data)):  
        item = plotWidget.plotDataItems[t]
        
        # Copy attributes and add some new ones
        attrs = item.attrs
        attrs['smooth_window_type'] = window
        attrs['smooth_window_length'] = window_len
        
        # Smooth
        traceSmooth = smooth.smooth(data[t], window_len=window_len, window=window)
        results.append([item.text(0), traceSmooth, attrs])
        
        # Plot smoothed trace
        x = np.arange(0, len(traceSmooth)*dt, dt)
        plotWidget.plot(x, traceSmooth, pen=pg.mkPen('#F2EF44', width=1))

    # Store results
    parentText = plotWidget.plotDataItems[0].parent().text(0) # Assumes all plotted data have the same parent
    aux.save_results(browser, parentText+'_smooth', results)           
    
    



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    








