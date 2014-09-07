""" Functions for managing trees
"""

import sys, os, re, copy
import sip
import h5py
from widgets import h5Item
from PyQt4 import QtGui, QtCore


def add_treeGroup(browser, tree, level, name):
    if level=='root':
        item = h5Item([name])
        parentWidget = browser.ui.workingDataTree.invisibleRootItem()
        browser.make_nameUnique(parentWidget, item, name)
        tree.addTopLevelItem(item)        
    elif level=='child':
        item = h5Item([name])
        parentWidget = tree.currentItem()
        browser.make_nameUnique(parentWidget, item, name) 
        parentWidget.addChild(item)

def rename_treeItem(browser, tree, text):
    item = tree.currentItem()    
    parentWidget = item.parent()
    if not parentWidget:  # item in top level
        parentWidget = browser.ui.workingDataTree.invisibleRootItem()
    browser.make_nameUnique(parentWidget, item, text)
    
def remove_treeItem(browser, tree):
    items = tree.selectedItems()
    for item in items:       
        sip.delete(item)

def set_loadFolder(browser, tree, homeFolder):
    tree.model.setRootPath(QtCore.QDir.absolutePath(QtCore.QDir(homeFolder)))
    tree.setRootIndex(tree.model.index(QtCore.QDir.absolutePath(QtCore.QDir(homeFolder))))      
