import sys, os, re, copy
import h5py

from PyQt4 import QtGui
from PyQt4 import QtCore
import sip

import numpy as np
import matplotlib.pyplot as plt

from browser import Ui_MainWindow
from h5TreeWidgetFile import h5Item

# Classes and main loop functions 
# -----------------------------------------------
class dataBrowser(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        # General Window settings
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
              
        # Directory browser
        model = QtGui.QFileSystemModel()
        model.setRootPath(QtCore.QDir.absolutePath(QtCore.QDir('/home/tiago/Code/py/hdf5/')))
        model.setNameFilters(['*.hdf5'])
        self.ui.dirTree.setModel(model)
        self.ui.dirTree.setColumnHidden(1, True)
        self.ui.dirTree.setColumnHidden(2, True)
        self.ui.dirTree.setColumnHidden(3, True)
        self.ui.dirTree.setRootIndex(model.index(QtCore.QDir.absolutePath(QtCore.QDir('/home/tiago/Code/py/hdf5/'))))
   
        self.ui.dirTree.selectionModel().selectionChanged.connect(self.loadH5OnSelectionChanged)
        self.currentFile = []
        
        # hdf5 browser
        self.ui.hdfTree.setColumnCount(1)
        self.ui.hdfTree.setHeaderLabels(['Data'])
        self.ui.hdfTree.currentItemChanged.connect(self.plotOnSelectionChanged)
        self.ui.hdfTree.itemSelectionChanged.connect(self.storeSelection)
        
        # working hdf5 tree
        self.ui.workingTree.setColumnCount(1)
        self.ui.workingTree.setHeaderLabels(['Working Data'])
        self.ui.actionLoadData.triggered.connect(self.loadH5OnLoadPush)
        self.ui.actionNewFile.triggered.connect(self.createH5OnNewPush)
        self.connect(self.ui.workingTree, QtCore.SIGNAL('dropped'), self.moveItemsAcross)
        self.connect(self.ui.workingTree, QtCore.SIGNAL('targetPosition'), self.setTargetPosition)
        
        # context menus
        self.ui.workingTree.customContextMenuRequested.connect(self.openWorkingTreeMenu)
        self.ui.actionAddRootGroup.triggered.connect(self.addRootGroupOnMenu)
        self.ui.actionAddChildGroup.triggered.connect(self.addChildGroupOnMenu)
        self.ui.actionRenameTreeItem.triggered.connect(self.renameItemOnMenu)
        self.ui.actionRemoveTreeItem.triggered.connect(self.removeItemOnMenu)
        
        # main plotting mouse actions
        self.ui.plotsWidget.insertNavigationBar(self)
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionPlotData)
        self.ui.actionPlotData.triggered.connect(self.plotSelected)
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionShowCursors)
        self.ui.actionShowCursors.toggled.connect(self.showCursors)
        
        self.mouseIsPressed = False
        cidPress = self.ui.plotsWidget.canvas.mpl_connect('button_press_event', self.on_press)
        cidMotion = self.ui.plotsWidget.canvas.mpl_connect('motion_notify_event', self.on_motion)        
        cidRelease = self.ui.plotsWidget.canvas.mpl_connect('button_release_event', self.on_release)    
                
        self.show()              
    
    # Tree methods
    def openWorkingTreeMenu(self, position):
        self.workingTreeMenu = QtGui.QMenu()
        self.workingTreeMenu.addAction(self.ui.actionAddRootGroup)
        self.workingTreeMenu.addAction(self.ui.actionAddChildGroup)
        self.workingTreeMenu.addAction(self.ui.actionAddDataset)
        self.workingTreeMenu.addAction(self.ui.actionRenameTreeItem)
        self.workingTreeMenu.addAction(self.ui.actionRemoveTreeItem)

        if len(self.ui.workingTree.selectedItems())==0: 
            self.ui.actionAddChildGroup.setDisabled(True)
            self.ui.actionRenameTreeItem.setDisabled(True)
        else:
            self.ui.actionAddChildGroup.setDisabled(False)
            self.ui.actionRenameTreeItem.setDisabled(False)
            
        self.workingTreeMenu.exec_(self.ui.workingTree.viewport().mapToGlobal(position))
    
    def loadH5OnSelectionChanged(self, newSelection, oldSelection):
        loadH5(self, self.ui.hdfTree)
       
    def loadH5OnLoadPush(self):
        loadH5(self, self.ui.workingTree)
        
    def createH5OnNewPush(self):
        createH5(self, self.ui.workingTree)

    def addRootGroupOnMenu(self):
        addTreeGroup(self, self.ui.workingTree, 'root')
       
    def addChildGroupOnMenu(self):
        addTreeGroup(self, self.ui.workingTree, 'child')
    
    def renameItemOnMenu(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Rename item', 'Enter new name:')
        if ok: renameTreeItem(self, self.ui.workingTree, str(text))

    def removeItemOnMenu(self):
        removeTreeItem(self, self.ui.workingTree)
    
    def storeSelection(self):
        self.dragItems = []
        for item in self.ui.hdfTree.selectedItems():
            self.dragItems.append([item.path, item.text(0)])        
    
    def setTargetPosition(self, parent, row):
        self.dragTargetParent = parent
        self.dragTargetRow = row
    
    def moveItemsAcross(self):
        targetItems = []
        for item in self.dragItems:
            i = h5Item([str(item[1])])
            i.path = item[0]
            targetItems.append(i)            
        
        parentIndex = self.ui.workingTree.indexFromItem(self.dragTargetParent)
        for row in np.arange(0, len(self.dragItems)):
            index = self.ui.workingTree.model().index(self.dragTargetRow+row, 0, parentIndex)        
            temp_item = self.ui.workingTree.itemFromIndex(QtCore.QModelIndex(index))
            sip.delete(temp_item)        
            if parentIndex.isValid():
                self.dragTargetParent.insertChild(index.row(), targetItems[row])
            else:
                self.ui.workingTree.insertTopLevelItem(index.row(), targetItems[row])     

        
    # Plot methods
    def plotOnSelectionChanged(self, current, previous):
        if current:
            if 'dataset' in str(self.db[current.path]):
                plotSingleData(self, self.ui.dataPlotWidget, self.db[current.path][:])
    
    def plotSelected(self):
        plotMultipleData(self, self.ui.plotsWidget)   
    
    def showCursors(self):
        if self.ui.plotsWidget.toolbar._active=="ZOOM": self.ui.plotsWidget.toolbar.zoom()  
        if self.ui.plotsWidget.toolbar._active=="PAN": self.ui.plotsWidget.toolbar.pan()      
        if self.ui.actionShowCursors.isChecked():
            self.ui.plotsWidget.createCursor()
            self.ui.plotsWidget.initCursor()
        else:
            self.ui.plotsWidget.hideCursor()
    
    def on_press(self, event):        
        if (event.button==1) & (self.ui.actionShowCursors.isChecked()):
          if (self.ui.plotsWidget.toolbar._active<>"PAN") & (self.ui.plotsWidget.toolbar._active<>"ZOOM"):
            self.mouseIsPressed = True
            self.ui.plotsWidget.showCursor(event)
        elif (event.button==3) & (self.ui.actionShowCursors.isChecked()):
            self.mouseIsPressed = True        
            self.ui.plotsWidget.refreshCursor(event)

    def on_release(self, event):        
        self.mouseIsPressed = False
        
    def on_motion(self, event):
        if (self.ui.plotsWidget.toolbar._active<>"PAN") & (self.ui.plotsWidget.toolbar._active<>"ZOOM"):         
          if self.mouseIsPressed:
            if (event.button==1) & (self.ui.actionShowCursors.isChecked()):
                self.ui.plotsWidget.showCursor(event)
            elif (event.button==3) & (self.ui.actionShowCursors.isChecked()):
                self.ui.plotsWidget.refreshCursor(event)

def main():    
    app = QtGui.QApplication(sys.argv)
    c = dataBrowser()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    



# Suport functions 
# -----------------------------------------------
# Plotting
def plotSingleData(browser, plotWidget, data):
    plotWidget.canvas.ax.clear()
    plotWidget.canvas.ax.plot(data, 'k')
    plotWidget.canvas.draw()

def plotMultipleData(browser, plotWidget):
    plotWidget.canvas.ax.clear()
    items = browser.ui.workingTree.selectedItems()
    if items:
        for item in items:
            if 'dataset' in str(browser.db[str(item.path)]):
                plotWidget.canvas.ax.plot(browser.db[str(item.path)][:], 'k')
    plotWidget.canvas.draw()            
    plotWidget.background = plotWidget.canvas.copy_from_bbox(plotWidget.canvas.ax.bbox)
    plotWidget.createCursor()
    if browser.ui.actionShowCursors.isChecked(): 
        plotWidget.showCursorLastPos()                 

# Tree management
def loadH5(browser, tree):
    index = browser.ui.dirTree.selectedIndexes()[0]
    currentFile = str(index.model().filePath(index))
    if '.hdf5' in currentFile:
        #print self.currentFile
        tree.clear()       
        browser.db = h5py.File(currentFile, 'r')
       
       # Insert groups into the tree
        for group in browser.db:
            item = h5Item([str(group)])
            item.path = '/'+str(group)
            tree.addTopLevelItem(item)
            populateH5tree(browser, browser.db['/'+str(group)], parentWidget=item) 

def populateH5tree(browser, parent, parentWidget):
    if isinstance(parent, h5py.Group):
        for child in parent:
            #print parent[child]
            item = h5Item([child])
            item.path = re.findall('"([^"]*)"', str(parent))[0] + '/' + str(child)
            parentWidget.addChild(item)
            populateH5tree(browser, parent[child], item)

def createH5(browser, tree):
    tree.clear()

def addTreeGroup(browser, tree, level):
    if level=='root':
        item = h5Item(['Group'])
        tree.addTopLevelItem(item) 
    elif level=='child':
        item = h5Item(['Group'])
        parentWidget = tree.currentItem()
        parentWidget.addChild(item)

def renameTreeItem(browser, tree, text):
    item = tree.currentItem()
    item.setText(0, text)
    
def removeTreeItem(browser, tree):
    items = tree.selectedItems()
    for item in items: sip.delete(item)







