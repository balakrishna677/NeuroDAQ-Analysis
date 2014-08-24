import sys, os, re, copy
import h5py

from PyQt4 import QtGui
from PyQt4 import QtCore
import sip

import numpy as np
import matplotlib.pyplot as plt

from browser import Ui_MainWindow
from h5TreeWidgetFile import h5Item

import analysisLib as alib 

# Classes and main loop functions 
# -----------------------------------------------
class dataBrowser(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        # General Window settings
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = None
        self.wdb = None
              
        # Directory browser
        self.model = QtGui.QFileSystemModel()
        #self.model.setRootPath(QtCore.QDir.absolutePath(QtCore.QDir('/home/tiago/Code/py/NeuroDAQ-Analysis/testData/')))
        self.model.setRootPath(QtCore.QDir.absolutePath(QtCore.QDir('/Users/adam/')))       
        self.model.setNameFilters(['*.hdf5'])
        self.ui.dirTree.setModel(self.model)
        self.ui.dirTree.setColumnHidden(1, True)
        self.ui.dirTree.setColumnHidden(2, True)
        self.ui.dirTree.setColumnHidden(3, True)
        #self.ui.dirTree.setRootIndex(self.model.index(QtCore.QDir.absolutePath(QtCore.QDir('/home/tiago/Code/py/NeuroDAQ-Analysis/testData/'))))
        self.ui.dirTree.setRootIndex(self.model.index(QtCore.QDir.absolutePath(QtCore.QDir('/Users/adam'))))   
        self.ui.dirTree.selectionModel().selectionChanged.connect(self.loadH5OnSelectionChanged)      #### not in Class ####
        self.currentOpenFile = []
        self.currentSaveFile = []
        
        # hdf5 browser
        self.ui.hdfTree.data = []
        self.ui.hdfTree.setColumnCount(1)
        self.ui.hdfTree.setHeaderLabels(['Data'])
        self.ui.hdfTree.currentItemChanged.connect(self.plotOnSelectionChanged)
        self.ui.hdfTree.itemSelectionChanged.connect(self.storeSelection)
        
        # working hdf5 tree
        self.ui.workingTree.data = []
        self.ui.workingTree.setColumnCount(1)
        self.ui.workingTree.setHeaderLabels(['Working Data'])
        self.ui.actionLoadData.triggered.connect(self.loadH5OnLoadPush)
        self.ui.actionNewFile.triggered.connect(self.createH5OnNewPush)
        self.ui.actionSaveFile.triggered.connect(self.saveH5OnSavePush)
        self.ui.actionSaveFileAs.triggered.connect(self.saveH5OnSaveAsPush)
        self.connect(self.ui.workingTree, QtCore.SIGNAL('dropped'), self.moveItemsAcross)
        self.connect(self.ui.workingTree, QtCore.SIGNAL('targetPosition'), self.setTargetPosition)
        self.ui.workingTree.propsDt = ''
        self.ui.workingTree.propsDescription = ''   
        
        # context menus
        self.ui.workingTree.customContextMenuRequested.connect(self.openWorkingTreeMenu)
        self.ui.actionAddRootGroup.triggered.connect(self.addRootGroupOnMenu)
        self.ui.actionAddChildGroup.triggered.connect(self.addChildGroupOnMenu)
        self.ui.actionRenameTreeItem.triggered.connect(self.renameItemOnMenu)
        self.ui.actionRemoveTreeItem.triggered.connect(self.removeItemOnMenu)
        self.ui.actionShowInTable.triggered.connect(self.showInTableOnMenu)        
        
        # properties table        
        self.ui.propsTableWidget.setRowCount(2)
        self.ui.propsTableWidget.setColumnCount(1)
        self.ui.propsTableWidget.horizontalHeader().setVisible(False)
        self.ui.workingTree.propsItemDtLabel = QtGui.QTableWidgetItem('dt')
        self.ui.workingTree.propsItemDt = QtGui.QTableWidgetItem(self.ui.workingTree.propsDt)
        self.ui.workingTree.propsItemDescriptionLabel = QtGui.QTableWidgetItem('Description')
        self.ui.workingTree.propsItemDescription = QtGui.QTableWidgetItem(self.ui.workingTree.propsDescription)                
        self.ui.propsTableWidget.setVerticalHeaderItem(0, self.ui.workingTree.propsItemDtLabel)
        self.ui.propsTableWidget.setItem(0,0,self.ui.workingTree.propsItemDt)
        self.ui.propsTableWidget.setVerticalHeaderItem(1, self.ui.workingTree.propsItemDescriptionLabel)
        self.ui.propsTableWidget.setItem(1,0,self.ui.workingTree.propsItemDescription)
        self.ui.propsTableWidget.cellChanged.connect(self.updateTableEntry)        
        
        # data table
        self.ui.dataTableWidget.setRowCount(100)
        self.ui.dataTableWidget.setColumnCount(100)
                
        # main plotting mouse actions
        self.ui.plotsWidget.plotDataIndex = None
        self.ui.plotsWidget.insertNavigationBar(self)
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionPlotData)
        self.ui.actionPlotData.triggered.connect(self.plotSelected)
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionShowCursors)
        self.ui.actionShowCursors.toggled.connect(self.showCursors)
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionZoomOut)
        self.ui.actionZoomOut.triggered.connect(self.zoomOut)
        self.mouseIsPressed = False
        cidPress = self.ui.plotsWidget.canvas.mpl_connect('button_press_event', self.on_press)
        cidMotion = self.ui.plotsWidget.canvas.mpl_connect('motion_notify_event', self.on_motion)        
        cidRelease = self.ui.plotsWidget.canvas.mpl_connect('button_release_event', self.on_release)    
        
        # analysis actions
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionBaseline)
        self.ui.actionBaseline.triggered.connect(self.baseline)
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionAverage)
        self.ui.actionAverage.triggered.connect(self.average)
        self.ui.plotsWidget.toolbar.addAction(self.ui.actionStats)
        self.ui.actionStats.triggered.connect(self.measureStats)        
                
        self.show()              
    
    # Tree methods
    def openWorkingTreeMenu(self, position):
        self.workingTreeMenu = QtGui.QMenu()
        self.workingTreeMenu.addAction(self.ui.actionAddRootGroup)
        self.workingTreeMenu.addAction(self.ui.actionAddChildGroup)
        self.workingTreeMenu.addAction(self.ui.actionAddDataset)
        self.workingTreeMenu.addAction(self.ui.actionRenameTreeItem)
        self.workingTreeMenu.addAction(self.ui.actionRemoveTreeItem)
        self.workingTreeMenu.addAction(self.ui.actionShowInTable)

        if len(self.ui.workingTree.selectedItems())==0: 
            self.ui.actionAddChildGroup.setDisabled(True)
            self.ui.actionRenameTreeItem.setDisabled(True)
        else:
            self.ui.actionAddChildGroup.setDisabled(False)
            self.ui.actionRenameTreeItem.setDisabled(False)
            
        self.workingTreeMenu.exec_(self.ui.workingTree.viewport().mapToGlobal(position))
    
    def loadH5OnSelectionChanged(self, newSelection, oldSelection):
        #newIndex = newSelection.indexes()[0]
        #oldIndex = oldSelection.indexes()[0]
        #currentFile = str(newIndex.model().filePath(newIndex))
        #oldFile = str(newIndex.model().filePath(newIndex))
        if self.db: 
            self.db.close()
            self.db = None
        loadH5(self, self.ui.hdfTree, push=False)
       
    def loadH5OnLoadPush(self):
        loadH5(self, self.ui.workingTree, push=True)
        
    def createH5OnNewPush(self):
        createH5(self, self.ui.workingTree)

    def saveH5OnSavePush(self):
        if self.currentSaveFile:
            saveH5(self, self.ui.workingTree)
        else: 
            fname, ok = QtGui.QInputDialog.getText(self, 'New file', 'Enter file name:')
            if ok:
                self.currentSaveFile = str(self.model.rootPath()) + '/' + fname + '.hdf5'
                saveH5(self, self.ui.workingTree)
        
    def saveH5OnSaveAsPush(self):
        fname, ok = QtGui.QInputDialog.getText(self, 'New file', 'Enter file name:')
        if ok:
            savePath = '/Users/adam/DataAnalysis'
            self.currentSaveFile = savePath + '/' + fname + '.hdf5'      
            #self.currentSaveFile = str(self.model.rootPath()) + '/' + fname + '.hdf5'
            saveH5(self, self.ui.workingTree)

    def addRootGroupOnMenu(self):
        addTreeGroup(self, self.ui.workingTree, 'root')
       
    def addChildGroupOnMenu(self):
        addTreeGroup(self, self.ui.workingTree, 'child')
    
    def renameItemOnMenu(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Rename item', 'Enter new name:')
        if ok: renameTreeItem(self, self.ui.workingTree, str(text))

    def removeItemOnMenu(self):
        removeTreeItem(self, self.ui.workingTree)

    def showInTableOnMenu(self):
        clearTable(self)
        putDataOnTable(self)
    
    def storeSelection(self):
        self.dragItems = []
        #for item in self.ui.hdfTree.selectedItems():
        #    self.dragItems.append([item.path, item.text(0), item.dataIndex])    
        for originalIndex in self.ui.hdfTree.selectedIndexes():
            item = self.ui.workingTree.itemFromIndex(QtCore.QModelIndex(originalIndex))
            self.dragItems.append([item.path, item.text(0), item.dataIndex, originalIndex]) 
    
    def setTargetPosition(self, parent, row):
        self.dragTargetParent = parent
        self.dragTargetRow = row
    
    def moveItemsAcross(self):
        targetItems = []
        for item in self.dragItems:
            i = h5Item([str(item[1])])
            i.path = item[0]
            i.dataIndex = item[2]
            i.originalIndex = item[3]
            targetItems.append(i)            
        
        parentIndex = self.ui.workingTree.indexFromItem(self.dragTargetParent)
        for row in np.arange(0, len(self.dragItems)):
            index = self.ui.workingTree.model().index(self.dragTargetRow+row, 0, parentIndex)        
            temp_item = self.ui.workingTree.itemFromIndex(QtCore.QModelIndex(index))
            sip.delete(temp_item)        
            if parentIndex.isValid():
                self.dragTargetParent.insertChild(index.row(), targetItems[row])
                originalParentWidget = self.ui.hdfTree.itemFromIndex(QtCore.QModelIndex(targetItems[row].originalIndex))
                populateH5dragItems(self, originalParentWidget, targetItems[row])
            else:
                self.ui.workingTree.insertTopLevelItem(index.row(), targetItems[row])     
                originalParentWidget = self.ui.hdfTree.itemFromIndex(QtCore.QModelIndex(targetItems[row].originalIndex))
                populateH5dragItems(self, originalParentWidget, targetItems[row])

    # Properties methods
    def updateTableEntry(self, row, col):
        if row==0: self.ui.workingTree.propsDt = self.ui.propsTableWidget.item(row, col).text() 
        if row==1: self.ui.workingTree.propsDescription = self.ui.propsTableWidget.item(row, col).text() 
        
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

    def zoomOut(self):
        if self.ui.plotsWidget.homeAxis: 
            self.ui.plotsWidget.canvas.ax.axis(self.ui.plotsWidget.homeAxis)
            self.ui.plotsWidget.cursor1.set_visible(False)
            self.ui.plotsWidget.cursor2.set_visible(False)
            self.ui.plotsWidget.canvas.draw()
            self.ui.plotsWidget.background = self.ui.plotsWidget.canvas.copy_from_bbox(self.ui.plotsWidget.canvas.ax.bbox)                 
            if self.ui.actionShowCursors.isChecked():
                x1,x2,y1,y2 = self.ui.plotsWidget.canvas.ax.axis()
                self.ui.plotsWidget.cursor1.set_data([self.ui.plotsWidget.cursor1Pos, self.ui.plotsWidget.cursor1Pos], [y1,y2])         
                self.ui.plotsWidget.cursor2.set_data([self.ui.plotsWidget.cursor2Pos, self.ui.plotsWidget.cursor2Pos], [y1,y2]) 
                self.ui.plotsWidget.cursor1.set_visible(True)
                self.ui.plotsWidget.cursor2.set_visible(True)
                self.ui.plotsWidget.canvas.ax.draw_artist(self.ui.plotsWidget.cursor1)
                self.ui.plotsWidget.canvas.ax.draw_artist(self.ui.plotsWidget.cursor2)
            self.ui.plotsWidget.canvas.draw()                     
    
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

    # Analysis methods
    def baseline(self):
        if self.ui.plotsWidget.plotDataIndex:
            if self.ui.plotsWidget.cursor1Pos: alib.baseline(self)

    def average(self):
        if self.ui.plotsWidget.plotDataIndex: alib.average(self)
        
    def measureStats(self):
        if self.ui.plotsWidget.plotDataIndex:
            if self.ui.plotsWidget.cursor1Pos: alib.measureStats(self)    
            
def main():    
    defaultFont = QtGui.QFont('Ubuntu', 8) 
    app = QtGui.QApplication(sys.argv)
    app.setFont(defaultFont)
    c = dataBrowser()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    



# Suport functions 
# -----------------------------------------------
# Plotting
def plotSingleData(browser, plotWidget, data):
    plotWidget.canvas.ax.clear()
    plotWidget.canvas.ax.plot(data, 'k', linewidth=0.5)
    plotWidget.canvas.draw()

def plotMultipleData(browser, plotWidget):
    dt = 0.04
    plotWidget.canvas.ax.clear()
    plotWidget.plotDataIndex = []
    items = browser.ui.workingTree.selectedItems()
    if items:
        for item in items:
            if item.dataIndex is not None:
                x = np.arange(0, len(browser.ui.workingTree.data[item.dataIndex])*dt, dt)
                plotWidget.canvas.ax.plot(x, browser.ui.workingTree.data[item.dataIndex], 'k', linewidth=0.5)
                plotWidget.plotDataIndex.append(item.dataIndex)
            #if 'dataset' in str(browser.db[str(item.path)]):
            #    plotWidget.canvas.ax.plot(browser.db[str(item.path)][:], 'k')
    plotWidget.canvas.draw()            
    plotWidget.background = plotWidget.canvas.copy_from_bbox(plotWidget.canvas.ax.bbox)
    plotWidget.createCursor()
    if browser.ui.actionShowCursors.isChecked(): 
        plotWidget.showCursorLastPos()                 
    browser.ui.plotsWidget.homeAxis = browser.ui.plotsWidget.canvas.ax.axis()

# Tree management
def loadH5(browser, tree, push):
    browser.ui.hdfTree.data = []
    index = browser.ui.dirTree.selectedIndexes()[0]
    currentFile = str(index.model().filePath(index))
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
            populateH5tree(browser, browser.db['/'+str(group)], parentWidget=item, push=push) 

    if push:
        browser.ui.workingTree.propsDt = ''
        browser.ui.workingTree.propsDescription = ''
        for attr in browser.db.attrs:
            #print attr, browser.db.attrs[attr]
            if 'dt' in attr: browser.ui.workingTree.propsDt = str(browser.db.attrs[attr])
            if 'description' in attr:  browser.ui.workingTree.propsDescription = browser.db.attrs[attr]
        updateTable(browser)
        browser.currentOpenFile = currentFile
        browser.currentSaveFile = currentFile
        browser.ui.workingTree.setHeaderLabels([os.path.split(currentFile)[1]])

def populateH5tree(browser, parent, parentWidget, push):
    if isinstance(parent, h5py.Group):
        for child in parent:
            #print parent[child]
            item = h5Item([child])
            item.path = re.findall('"([^"]*)"', str(parent))[0] + '/' + str(child)
            parentWidget.addChild(item)
            populateH5tree(browser, parent[child], item, push)
    elif isinstance(parent, h5py.Dataset):
        if push:
            parentWidget.dataIndex = len(browser.ui.workingTree.data)
            browser.ui.workingTree.data.append(parent[:])

def populateH5File(browser, parent, parentWidget):
    for i in range(parentWidget.childCount()):
        item = parentWidget.child(i)        
        if item.childCount()>0:
            parent.create_group(str(item.text(0)))
            populateH5File(browser, parent[str(item.text(0))], parentWidget=item)
        else:
            parent.create_dataset(str(item.text(0)), data=browser.ui.workingTree.data[item.dataIndex])

def populateH5dragItems(browser, originalParentWidget, parentWidget):
    if originalParentWidget.childCount()>0:
        for c in range(originalParentWidget.childCount()):
            child = originalParentWidget.child(c)
            i = h5Item([str(child.text(0))])
            i.path = child.path
            parentWidget.addChild(i)
            if child.childCount()>0:
                populateH5dragItems(browser, child, i)
            else:
                i.dataIndex = len(browser.ui.workingTree.data)
                browser.ui.workingTree.data.append(browser.db[child.path][:])


def createH5(browser, tree):
    fname, ok = QtGui.QInputDialog.getText(browser, 'New file', 'Enter file name:')
    if ok: 
        browser.ui.workingTree.data = []
        tree.clear()
        browser.ui.workingTree.saveStr = fname     
        browser.ui.workingTree.propsDt = ''
        browser.ui.workingTree.propsDescription = ''   
        updateTable(browser)
        browser.ui.workingTree.setHeaderLabels([fname])
        savePath = '/Users/adam/DataAnalysis'
        #browser.currentSaveFile = str(browser.model.rootPath()) + '/' + fname + '.hdf5'
        browser.currentSaveFile = savePath + '/' + fname + '.hdf5'           

def saveH5(browser, tree):
    currentSaveFile = str(browser.currentSaveFile)
    currentOpenFile = str(browser.currentOpenFile)
    browser.ui.workingTree.setHeaderLabels([os.path.split(currentSaveFile)[1]])
    #pathName = str(browser.model.rootPath()) + '/' + fname + '.hdf5'
    if browser.db:
        browser.db.close()
        browser.db = None
    browser.wdb = h5py.File(currentSaveFile, 'w')
    root = tree.invisibleRootItem()
    childCount = root.childCount()
    for i in range(childCount):
        item = root.child(i)
        browser.wdb.create_group(str(item.text(0)))
        populateH5File(browser, browser.wdb['/'+str(item.text(0))], item)
    browser.wdb.attrs['dt'] =  str(browser.ui.workingTree.propsDt) 
    browser.wdb.attrs['description'] =  str(browser.ui.workingTree.propsDescription)     
    browser.wdb.close()         
       
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
    for item in items: 
        #deleteDataIndexes(tree, item)        
        sip.delete(item)

# can't use this unless updating indexes of all other object, so right now just leave it
def deleteDataIndexes(tree, parentWidget):
    for c in range(parentWidget.childCount()):
        item = parentWidget.child(c)
        if item.childCount()>0:
            deleteDataIndexes(tree, parentWidget=item)
        else:
            del tree.data[item.dataIndex]


# Properties
def updateTable(browser):   
    browser.ui.workingTree.propsItemDt = QtGui.QTableWidgetItem(browser.ui.workingTree.propsDt)
    browser.ui.workingTree.propsItemDescription = QtGui.QTableWidgetItem(browser.ui.workingTree.propsDescription)                
    browser.ui.propsTableWidget.setItem(0,0,browser.ui.workingTree.propsItemDt)
    browser.ui.propsTableWidget.setItem(1,0,browser.ui.workingTree.propsItemDescription)

# Data Table
def putDataOnTable(browser):
    row, col = 0, 0
    items = browser.ui.workingTree.selectedItems()    
    if items:
        for item in items:
            if item.dataIndex is not None:
                addData(browser, row, col, browser.ui.workingTree.data[item.dataIndex])
            col+=1        

def addData(browser, row, col, data):
    for dpoint in range(len(data)):
        item = QtGui.QTableWidgetItem(str(data[dpoint]))
        browser.ui.dataTableWidget.setItem(row, col, item)
        row+=1    

def clearTable(browser):
    for row in range(100):
        for col in range(100):
            item = QtGui.QTableWidgetItem('')
            browser.ui.dataTableWidget.setItem(row, col, item) 
    

# TO DO:
# sorting of elements in tree (add 0 to numbers and have column for user defined orders) 
# time, dt in recordings 
# single plotting in data tree
# tidy zoom out function - try to draw just the axis instead of the whole thing again
# deal with poperties properly and attach them to Groups and Datasets

























