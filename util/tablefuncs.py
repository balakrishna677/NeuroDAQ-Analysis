""" Functions for managing tables
"""

import sys, os, re, copy
import numpy as np
import sip
import h5py
from PyQt4 import QtGui, QtCore

def put_dataOnTable(browser):
    #row, col = 0, 0
    dataList = []
    items = browser.ui.workingDataTree.selectedItems()    
    if items:
        for item in items:
            if item.dataIndex is not None:
                 data = browser.ui.workingDataTree.data[item.dataIndex]
                 dataList.append(data)
                 #browser.ui.dataTableWidget.setData([browser.ui.workingDataTree.data[item.dataIndex]])
                 #add_data(browser, row, col, browser.ui.workingDataTree.data[item.dataIndex])
            #col+=1        
    browser.ui.dataTableWidget.setData(dataList)

def add_data(browser, row, col, data):
    for dpoint in range(len(data)):
        item = QtGui.QTableWidgetItem(str(data[dpoint]))
        browser.ui.dataTableWidget.setItem(row, col, item)
        row+=1    

def clear_table(browser):
    for row in range(100):
        for col in range(100):
            item = QtGui.QTableWidgetItem('')
            browser.ui.dataTableWidget.setItem(row, col, item) 

def update_props(browser):   
    browser.ui.workingDataTree.propsItemDt = QtGui.QTableWidgetItem(browser.ui.workingDataTree.propsDt)
    browser.ui.workingDataTree.propsItemDescription = QtGui.QTableWidgetItem(browser.ui.workingDataTree.propsDescription)                
    browser.ui.propsTableWidget.setItem(0,0,browser.ui.workingDataTree.propsItemDt)
    browser.ui.propsTableWidget.setItem(1,0,browser.ui.workingDataTree.propsItemDescription)
