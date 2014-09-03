""" Functions for getting data in and out of .hdf5 files
and into H5 trees

Currently New File and Save As are saved to the folder currently
open in the file data tree.
"""

import sys, os, re, copy
import h5py
from PyQt4 import QtGui, QtCore
import sip
import numpy as np
from widgets import h5Item
import tablefuncs as table

def load_h5(browser, tree, push):
    browser.ui.fileDataTree.data = []
    index = browser.ui.dirTree.selectedIndexes()[0]
    currentFile = str(index.model().filePath(index))
    browser.currentFolder = os.path.dirname(currentFile)
    if browser.db: browser.db.close()
    if '.hdf5' in currentFile:
        #print self.currentFile
        browser.db = h5py.File(currentFile, 'r+')
        tree.clear()       
        # Insert groups into the tree and add data to internal data list
        for group in browser.db:
            item = h5Item([str(group)])
            item.path = '/'+str(group)
            tree.addTopLevelItem(item)
            populate_h5tree(browser, browser.db['/'+str(group)], parentWidget=item, push=push) 

    if push:
        browser.ui.workingDataTree.propsDt = ''
        browser.ui.workingDataTree.propsDescription = ''
        for attr in browser.db.attrs:
            #print attr, browser.db.attrs[attr]
            if 'dt' in attr: browser.ui.workingDataTree.propsDt = str(browser.db.attrs[attr])
            if 'description' in attr:  browser.ui.workingDataTree.propsDescription = browser.db.attrs[attr]
        table.update_table(browser)
        browser.currentOpenFile = currentFile
        browser.currentSaveFile = currentFile
        browser.ui.workingDataTree.setHeaderLabels([os.path.split(currentFile)[1]])


def populate_h5tree(browser, parent, parentWidget, push):
    if isinstance(parent, h5py.Group):
        for child in parent:
            #print parent[child]
            item = h5Item([child])
            item.path = re.findall('"([^"]*)"', str(parent))[0] + '/' + str(child)
            parentWidget.addChild(item)
            populate_h5tree(browser, parent[child], item, push)
    elif isinstance(parent, h5py.Dataset):
        if push:
            parentWidget.dataIndex = len(browser.ui.workingDataTree.data)
            browser.ui.workingDataTree.data.append(parent[:])


def populate_h5File(browser, parent, parentWidget):
    for i in range(parentWidget.childCount()):
        item = parentWidget.child(i)        
        if item.childCount()>0:
            parent.create_group(str(item.text(0)))
            populate_h5File(browser, parent[str(item.text(0))], parentWidget=item)
        else:
            parent.create_dataset(str(item.text(0)), data=browser.ui.workingDataTree.data[item.dataIndex])


def populate_h5dragItems(browser, originalParentWidget, parentWidget):
    if originalParentWidget.childCount()>0:
        for c in range(originalParentWidget.childCount()):
            child = originalParentWidget.child(c)
            i = h5Item([str(child.text(0))])
            i.path = child.path
            parentWidget.addChild(i)
            if child.childCount()>0:
                populate_h5dragItems(browser, child, i)
            else:
                i.dataIndex = len(browser.ui.workingDataTree.data)
                browser.ui.workingDataTree.data.append(browser.db[child.path][:])

def create_h5(browser, tree):
    fname, ok = QtGui.QInputDialog.getText(browser, 'New file', 'Enter file name:')
    if ok: 
        browser.ui.workingDataTree.data = []
        tree.clear()
        browser.ui.workingDataTree.saveStr = fname     
        browser.ui.workingDataTree.propsDt = ''
        browser.ui.workingDataTree.propsDescription = ''   
        table.update_table(browser)
        browser.ui.workingDataTree.setHeaderLabels([fname])
        browser.currentSaveFile = browser.currentFolder + '/' + fname + '.hdf5'           


def save_h5(browser, tree):
    currentSaveFile = str(browser.currentSaveFile)
    browser.ui.workingDataTree.setHeaderLabels([os.path.split(currentSaveFile)[1]])
    if browser.db:
        browser.db.close()
        browser.db = None
    browser.wdb = h5py.File(currentSaveFile, 'w')
    root = tree.invisibleRootItem()
    childCount = root.childCount()
    for i in range(childCount):
        item = root.child(i)
        browser.wdb.create_group(str(item.text(0)))
        populate_h5File(browser, browser.wdb['/'+str(item.text(0))], item)
    browser.wdb.attrs['dt'] =  str(browser.ui.workingDataTree.propsDt) 
    browser.wdb.attrs['description'] =  str(browser.ui.workingDataTree.propsDescription)     
    browser.wdb.close()
