""" Functions for managing tables
"""

import sys, os, re, copy
import numpy as np
import sip
import h5py
from PyQt4 import QtGui, QtCore

def put_dataOnTable_old(browser):
    dataList = []
    items = browser.ui.workingDataTree.selectedItems()    
    if items:
        for item in items:
             dataList.append(item.data) 
    browser.ui.dataTableWidget.setData(dataList)

def put_dataOnTable(browser, table):
    items = browser.ui.workingDataTree.selectedItems()
    startCol = 0
    #if items:
    #    for item in items:
    #        d

def add_data(browser, row, col, data):
    for dpoint in range(len(data)):
        item = QtGui.QTableWidgetItem(str(data[dpoint]))
        browser.ui.dataTableWidget.setItem(row, col, item)
        row+=1    

def clear_table(browser):
    browser.ui.dataTableWidget.clear() 

def update_props(browser):   
    browser.ui.workingDataTree.propsItemDt = QtGui.QTableWidgetItem(browser.ui.workingDataTree.propsDt)
    browser.ui.workingDataTree.propsItemDescription = QtGui.QTableWidgetItem(browser.ui.workingDataTree.propsDescription)                
    browser.ui.propsTableWidget.setItem(0,0,browser.ui.workingDataTree.propsItemDt)
    browser.ui.propsTableWidget.setItem(1,0,browser.ui.workingDataTree.propsItemDescription)
    
    
    
    
