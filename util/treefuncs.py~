""" Functions for managing trees
"""

import sys, os, re, copy
import sip
import h5py
from widgets import h5Item
from PyQt4 import QtGui, QtCore


def add_treeGroup(browser, tree, level):
    if level=='root':
        item = h5Item(['Group'])
        tree.addTopLevelItem(item)        
    elif level=='child':
        item = h5Item(['Group'])
        parentWidget = tree.currentItem()
        parentWidget.addChild(item)

def rename_treeItem(browser, tree, text):
    item = tree.currentItem()
    item.setText(0, text)
    
def remove_treeItem(browser, tree):
    items = tree.selectedItems()
    for item in items:       
        sip.delete(item)

def set_loadFolder(browser, tree, homeFolder):
    tree.model.setRootPath(QtCore.QDir.absolutePath(QtCore.QDir(homeFolder)))
    tree.setRootIndex(tree.model.index(QtCore.QDir.absolutePath(QtCore.QDir(homeFolder))))      
