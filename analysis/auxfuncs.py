""" Auxiliary analysis functions for 1D data

Data is collected from the currently plotted traces (or selection later)
in a list that is converted into a numpy array. To access attributes of
the trace, such as dt, we also need to match the data to the h5item where
it comes from, so currently plotted items are stored in plotWidget.plotDataItems
(in pgfuncs.py). The items are stored in a list assembled in the same order
as the data list, so the indexes match.
"""

import numpy as np
import os
import traceback
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from widgets import h5Item, h5TreeWidget, h5itemSelect
from util import pgplot
    

def get_data(browser):
    """ Return the data currently plotted.
    """
    data = []
    for item in browser.ui.dataPlotsWidget.plotDataItems:
        #data.append(browser.ui.workingDataTree.data[item.dataIndex])
        data.append(item.data)
    data = np.array(data)
    return data


def get_attr(itemsList, attr):
    """ Return a list with the values of attribute attr
    """
    attrList = []
    try:
        for item in itemsList:
            attrList.append(item.attrs[attr])
        return attrList
    except KeyError:
        print attr, 'not found'
    

def get_cursors(plotWidget):
    """ Return the current position of the data cursors
    in X-axis values.
    """
    c1 = plotWidget.cursor1.value()
    c2 = plotWidget.cursor2.value()
    plotWidget.cursor1Pos = c1     # Store positions for re-plotting
    plotWidget.cursor2Pos = c2    
    if c2<c1:        
        temp = c2
        c2 = c1
        c1 = temp
    #return int(c1/plotWidget.dt), int(c2/plotWidget.dt)
    return int(c1), int(c2)

def check_cursors(c1, c2, data, dt):
    """ Check that cursor positions are within data limits
    and coerce if necessary. Data is a 1D array.
    """
    if c1/dt < 0: c1 = 0
    if c2/dt > len(data) : c2 = (len(data)-1)*dt
    return c1, c2
    
def get_dataRange(plotWidget, item, cursors=False):
    """ Get plot item data within cursor limits or all
    data if there are no cursors. Coerce to data limits
    if cursors are out of data boundaries.
    
    Return data array and c1 position in datapoints for
    superimposing on original data if required. Optionally
    return cursor positions in data x-axis values.    
    """
    dt = item.attrs['dt']
    if plotWidget.cursor:
        c1 = int(plotWidget.cursor1.value()/dt)
        c2 = int(plotWidget.cursor2.value()/dt)  
        # Ensure c1 is less than c2  
        if c2<c1:        
            temp = c2
            c2 = c1
            c1 = temp
        # Coerce to data limits if necessary
        if c1 < 0: c1 = 0
        if c2 > len(item.data) : c2 = (len(item.data))        
    else:
        c1 = 0
        c2 = len(item.data)
    if cursors:
        return item.data[c1:c2], c1, c1*dt, c2*dt
    else:
        return item.data[c1:c2], c1    
    

def make_h5item(name, data, attrs):
    """ Makes a new h5item for general use 
    """
    item = h5Item([name])
    item.data = data
    item.attrs = attrs
    return item

def make_data_copy(browser, plotWidget):
    """ Make a copy of the currently plotted data to work on, 
    in order to keep the original data intact. Add new items
    to the working data tree and plot them. 
    """
    parentText = plotWidget.plotDataItems[0].parent().text(0)
    item = h5Item([parentText+'_OriginalCopy'])
    parentWidget = browser.ui.workingDataTree.invisibleRootItem()
    browser.make_nameUnique(parentWidget, item, item.text(0))
    browser.ui.workingDataTree.addTopLevelItem(item)
    childrenList = []     
    for plotItem in plotWidget.plotDataItems:
        # Add items to tree
        child = h5Item([str(plotItem.text(0))])
        browser.make_nameUnique(item, child, child.text(0))
        item.addChild(child)
        child.attrs = plotItem.attrs
        child.data = plotItem.data
        child.listIndex =  len(browser.ui.workingDataTree.dataItems)
        browser.ui.workingDataTree.dataItems.append(child)  
        childrenList.append(child)      

def plot_point(plotWidget, cursor1, xpoint, ypoint, dt):
    """ Plots a single point, with the X coordinate measured from the position
    of cursor 1 (i.e.: cursor 1 X-position = 0). Useful from when processing data
    within the cursor range and needing to plot the results on top of the entire trace.
    """
    x = (xpoint + cursor1) * dt
    plotWidget.plot([x], [ypoint], pen=None, symbol='o', symbolPen='r', symbolBrush=None, symbolSize=7)


def save_results(browser, parentText, results):
    """ Saves data to workingDataTree.data and adds
    corresponding entry in the tree with a parent at 
    root level and children.
    
    'results' is a list with n items ['label', data, attrs]    
    Returns a list with the list indexes of the stored items
    """        
    listIndexes = []
    item = h5Item([parentText])
    parentWidget = browser.ui.workingDataTree.invisibleRootItem()
    browser.make_nameUnique(parentWidget, item, item.text(0))        
    browser.ui.workingDataTree.addTopLevelItem(item)
    for result in results:
        child = h5Item([result[0]])
        browser.make_nameUnique(item, child, child.text(0))
        item.addChild(child)  
        if len(result)>2: child.attrs = result[2]
        child.listIndex =  len(browser.ui.workingDataTree.dataItems)
        listIndexes.append(child.listIndex)
        browser.ui.workingDataTree.dataItems.append(child)
        child.data = result[1]   
    return listIndexes


def error_box(text, errorInfo=None, infoText=None):    
    """ Displays a error message box with custom text and optional
    details of the error (including traceback) and additional information.
    """
    errorBox = QtGui.QMessageBox()
    errorBox.setWindowTitle('Error')
    errorBox.setText('<b>'+text+'</b>')
    errorBox.setIcon(QtGui.QMessageBox.Critical)
    # Get error and traceback info
    if errorInfo:
        error_type, error_value, error_traceback = errorInfo
        tracebackInfo = traceback.format_exception(error_type, error_value, error_traceback)
        errorBox.setDetailedText(''.join(tracebackInfo)) 
    # Add additional info
    if infoText:
        errorBox.setInformativeText(infoText)
    errorBox.exec_()

def warning_box(text, infoText=None):    
    """ Displays a warning message box with custom text and optional
    additional information.
    """
    warningBox = QtGui.QMessageBox()
    warningBox.setWindowTitle('Warning')
    warningBox.setText('<b>'+text+'</b>')
    warningBox.setIcon(QtGui.QMessageBox.Warning)
    # Add additional info
    if infoText:
        warningBox.setInformativeText(infoText)
    warningBox.exec_()
    
def selectItem_box(browser):
    """ Asks the user to select an item in the data tree for analysis
    """
    q = h5itemSelect(browser.ui.workingDataTree, 'Please select the data analyse')
    if q.exec_():
        return q.getItemPath()


def getTreePath(item):
    path = []
    while item is not None:
        path.append(str(item.text(0)))
        item = item.parent()
    return '/'.join(reversed(path))


def getItemFromPath(path, parent, level=0):
#path = path.split('/')
    """ Return the item corresponding to the path
    'path' is a list with the path elements in order
    """
    pathItem = None
    for i in range(parent.childCount()):
        item = parent.child(i)
        if item.text(0)==path[level]:
            if level<(len(path)-1):
                level+=1
                #print item.text(0), level
                return getItemFromPath(path, item, level)
            else:
                pathItem = item     
    return pathItem



