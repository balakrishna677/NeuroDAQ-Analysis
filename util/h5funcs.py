""" Functions for getting data in and out of .hdf5 files
and into H5 trees

Save overwrites the current file, New File and Save As are 
saved to the folder selected in the Save text input.

Attributes are attached to datasets only, not to groups (yet).
"""

import sys, os, re, copy
import h5py
from PyQt4 import QtGui, QtCore
import sip
import numpy as np
from widgets import h5Item
from nptdms import TdmsFile
import tablefuncs as table
import imagefuncs as imagefun

def load_h5(browser, tree, push):
    """ Main loading function. Initially written for .hdf5 files only,
    but now also load .tdms files. 
    
    The whole thing could use with consolidating the code, there
    is redundancy and some of the functionality is not necessary.
    """
    browser.ui.fileDataTree.data = []
    index = browser.ui.dirTree.selectedIndexes()[0]
    currentFile = str(index.model().filePath(index))
    browser.currentFolder = os.path.dirname(currentFile)
    browser.ui.loadFolderInput.setText(browser.currentFolder)

    if '.hdf5' in currentFile:
        if browser.db: browser.db.close()
        browser.db = h5py.File(currentFile, 'r+')
        browser.dbType = 'hdf5'
        tree.clear()       
        # Insert groups into the tree and add data to internal data list
        for group in browser.db:
            item = h5Item([str(group)])
            item.path = '/'+str(group)
            tree.addTopLevelItem(item)
            populate_h5tree(browser, browser.db['/'+str(group)], parentWidget=item, push=push) 
        # Select first item of loaded list
        tree.setCurrentItem(tree.itemAt(0,0))
        if push:
            browser.saveFolder = browser.currentFolder
            browser.ui.saveFolderInput.setText(browser.saveFolder)
            browser.ui.workingDataTree.setSortingEnabled(True)
            browser.ui.notesWidget.clear()
            for attr in browser.db.attrs:
                browser.ui.workingDataTree.root.attrs[attr] = browser.db.attrs[attr]
                if 'Notes' in attr: browser.ui.notesWidget.setText(browser.db.attrs['Notes'])
                #if 'dt' in attr: browser.ui.workingDataTree.propsDt = str(browser.db.attrs[attr])
                if 'description' in attr: browser.ui.propsTableWidget.setData({'Description':[browser.db.attrs['description']]})
                #table.update_props(browser)
            browser.currentOpenFile = currentFile
            browser.currentSaveFile = currentFile
            browser.ui.workingDataTree.setHeaderLabels([os.path.split(currentFile)[1]])
            browser.ui.workingDataTree.setSortingEnabled(False)  # Otherwise it screws up drag and drop

    if '.tdms' in currentFile:
        browser.db = TdmsFile(currentFile)
        browser.dbType = 'tdms'
        tree.clear()       
        # Deal with properties
        for attr in browser.db.object().properties:
            if 'kHz' in attr:
                browser.ui.fileDataTree.root.attrs['sampling_rate(kHz)'] = browser.db.object().properties[attr]
                if push:
                    browser.ui.workingDataTree.root.attrs['sampling_rate(kHz)'] = browser.db.object().properties[attr]
            elif 'pixel' in attr:
                imaging = True
            else:
                browser.ui.fileDataTree.root.attrs[attr] = browser.db.object().properties[attr]   
                if push:
                    browser.ui.workingDataTree.root.attrs[attr] = browser.db.object().properties[attr]        
        # Insert groups into the tree and add data to internal data list
        if push:
            imaging = False
            browser.saveFolder = browser.currentFolder      
            browser.ui.saveFolderInput.setText(browser.saveFolder)  
            browser.ui.workingDataTree.setSortingEnabled(True)
            browser.ui.notesWidget.clear()
            browser.currentOpenFile = currentFile
            browser.currentSaveFile = os.path.splitext(currentFile)[0]+'.hdf5'
            browser.ui.workingDataTree.setHeaderLabels([os.path.split(browser.currentSaveFile)[1]])
            browser.ui.workingDataTree.setSortingEnabled(False)  # Otherwise it screws up drag and drop
        for group in browser.db.groups():
            item = h5Item([str(group)])
            tree.addTopLevelItem(item)
            for channel in browser.db.group_channels(group):
                channelname = re.findall(r"'(.*?)'", channel.path , re.DOTALL)[1]
                child = h5Item([str(channelname)])
                child.group = group
                child.channel = channelname
                item.addChild(child)    
                if 'kHz' in str(tree.root.attrs): 
                    child.attrs['dt'] = 1./tree.root.attrs['sampling_rate(kHz)']                   
                if push:
                    child.data = get_dataFromFile(browser, child)
                    if imaging: 
                        imageArray = imagefun.array2image(child.data, (1024,1024))
                        child.data = imageArray
                    child.listIndex = len(browser.ui.workingDataTree.dataItems)
                    browser.ui.workingDataTree.dataItems.append(child)
                    #if 'kHz' in str(browser.ui.workingDataTree.root.attrs): 
                    #    child.attrs['dt'] = 1./browser.ui.workingDataTree.root.attrs['sampling_rate(kHz)']       


def populate_h5tree(browser, parent, parentWidget, push):   
    if isinstance(parent, h5py.Group):
        for child in parent:
            #print parent[child]
            item = h5Item([child])
            item.path = re.findall('"([^"]*)"', str(parent))[0] + '/' + str(child)
            parentWidget.addChild(item)
            populate_h5tree(browser, parent[child], item, push)
    elif isinstance(parent, h5py.Dataset):
        set_attrs(parent, parentWidget)
        if push:
            try:         
                parentWidget.data = get_dataFromFile(browser, parentWidget)
                parentWidget.listIndex = len(browser.ui.workingDataTree.dataItems)          
                browser.ui.workingDataTree.dataItems.append(parentWidget)
            except ValueError:   # No data in the dataset
                sip.delete(parentWidget)

def populate_h5File(browser, parent, parentWidget):
    for i in range(parentWidget.childCount()):
        item = parentWidget.child(i)        
        if item.childCount()>0:
            parent.create_group(str(item.text(0)))
            populate_h5File(browser, parent[str(item.text(0))], parentWidget=item)
        elif item.data is not None:
            dset = parent.create_dataset(str(item.text(0)), data=item.data)
            set_attrs(item, dset)
        else:
            parent.create_group(str(item.text(0)))

def populate_h5dragItems(browser, originalParentWidget, parentWidget):
    if originalParentWidget.childCount()>0:
        for c in range(originalParentWidget.childCount()):
            child = originalParentWidget.child(c)
            #itemName = make_nameUnique(parentWidget, child.text(0))
            i = h5Item([str(child.text(0))])
            i.path = child.path
            i.group = child.group
            i.channel = child.channel
            parentWidget.addChild(i)
            if child.childCount()>0:
                populate_h5dragItems(browser, child, i)
            else:
                set_attrs(child, i)
                i.listIndex = len(browser.ui.workingDataTree.dataItems)
                i.data = get_dataFromFile(browser, i)
                browser.ui.workingDataTree.dataItems.append(i)
    # For transferring datasets directly
    else:
        set_attrs(originalParentWidget, parentWidget)
        parentWidget.path = originalParentWidget.path
        parentWidget.listIndex = len(browser.ui.workingDataTree.dataItems)
        #browser.ui.workingDataTree.data.append(browser.db[originalParentWidget.path][:])
        parentWidget.data = browser.db[originalParentWidget.path][:]
        browser.ui.workingDataTree.dataItems.append(parentWidget)

def populate_h5copyItems(browser, originalParentWidget, parentWidget):
    if originalParentWidget.childCount()>0:
        for c in range(originalParentWidget.childCount()):
            child = originalParentWidget.child(c)
            #itemName = make_nameUnique(parentWidget, child.text(0))
            i = h5Item([str(child.text(0))])
            parentWidget.addChild(i)
            if child.childCount()>0:
                populate_h5copyItems(browser, child, i)
            else:
                set_attrs(child, i)
                i.listIndex = len(browser.ui.workingDataTree.dataItems)
                #browser.ui.workingDataTree.data.append(browser.db[child.path][:])
                i.data = child.data
                browser.ui.workingDataTree.dataItems.append(i)
    # For transferring datasets directly
    else:
        set_attrs(originalParentWidget, parentWidget)
        parentWidget.path = originalParentWidget.path
        parentWidget.listIndex = len(browser.ui.workingDataTree.dataItems)
        #browser.ui.workingDataTree.data.append(browser.db[originalParentWidget.path][:])
        parentWidget.data = originalParentWidget.data
        browser.ui.workingDataTree.dataItems.append(parentWidget)

def create_h5(browser, tree):
    fname, ok = QtGui.QInputDialog.getText(browser, 'New file', 'Enter file name:')
    if ok: 
        browser.ui.workingDataTree.data = []
        tree.clear()
        browser.ui.workingDataTree.saveStr = fname     
        browser.ui.workingDataTree.propsDt = ''
        browser.ui.workingDataTree.propsDescription = ''   
        #table.update_table(browser)
        browser.ui.workingDataTree.setHeaderLabels([fname])
        browser.currentSaveFile = browser.currentFolder + '/' + fname + '.hdf5'           


def save_h5(browser, tree):
  try:
    currentSaveFile = str(browser.currentSaveFile)
    browser.ui.workingDataTree.setHeaderLabels([os.path.split(currentSaveFile)[1]])
    if browser.db:
        #if browser.dbType=='hdf5':
        browser.db.close()
        browser.db = None
    if browser.wdb: browser.wdb.close()
    browser.wdb = h5py.File(currentSaveFile, 'w')
    root = tree.invisibleRootItem()
    populate_h5File(browser, browser.wdb['/'], root) 
    # File attributes
    set_attrs(browser.ui.workingDataTree.root, browser.wdb)   
    browser.wdb.attrs['Notes'] =  str(browser.ui.notesWidget.toPlainText())   
    browser.wdb.close()
  except:
    print 'Unexpected error, the data might have not been saved'
    raise

def set_attrs(source, item):
    """ Set attributes of h5 item or dataset
    Source and item can be tree h5item or h5File dataset, the syntax is the same.
    """
    for attr in source.attrs:
        if type(source.attrs[attr]) is unicode:
            item.attrs[attr] = str(source.attrs[attr])
        else:
            item.attrs[attr] = source.attrs[attr] 

def make_nameUnique(browser, parentWidget, name):
    """ Check existing names in parentWidget that start with 'name'
    and get the next available index, as 'name_index'.
    Returns 'name' if unique, or 'name_index'
    """
    name = str(name)
    if not parentWidget:
        parentWidget = browser.ui.workingDataTree.invisibleRootItem()
    if parentWidget.childCount()>0:
        #print 'there are', parentWidget.childCount(), 'children'
        existingNames = []
        for c in range(parentWidget.childCount()):
            child = parentWidget.child(c)
            s = str(child.text(0)).strip(name+'_')
            if not s:  # Name is the same, the strip operation gives ''
                existingNames.append(0)
            else:
                existingNames.append(int(s))
        if np.max(existingNames)>0:
            name = name + '_' + str(np.max(existingNames)+1)
    print existingNames
    print 'name is', name
    return name
    
def get_dataFromFile(browser, item):
    data = None
    if browser.dbType=='hdf5':
        if 'dataset' in str(browser.db[item.path]):
            data = browser.db[item.path][:]
    elif browser.dbType=='tdms':
        if item.channel:
            data = browser.db.object(item.group, item.channel).data
    return data




    
    

        

