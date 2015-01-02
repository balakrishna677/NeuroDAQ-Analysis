# Setup main interface
#
# Widgets and layouts are created by gui.py
#
# T.Branco @ MRC-LMB 2014
# -----------------------------------------------------------------------------

import sys, os, re, copy
import IPython

import h5py
import sip
import numpy as np

sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui, QtCore

from gui import Ui_MainWindow
from widgets import h5Item, tableItem
from util import h5, mplplot, treefun, table, pgplot, imagefun
from analysis import toolselector, auxfuncs, template
from console import utils as utilsconsole

import pyqtgraph as pg
from analysis.modules import *
from analysis.acq4 import filterfuncs as acq4filter
from analysis import moduleLoader

class NeuroDaqWindow(QtGui.QMainWindow):
    """ Assembles the main NeuroDAQ user interface.
    
    Data management:
    
    All H5 items that contain data are stored in workingDataTree.dataItems. The property 
    item.listIndex contains the location of the item on the list, so that it can be accessed
    programatically when needed.
    
    To keep track of data plotted in dataPlotsWidget, the items plotted are stored in
    dataPlotsWidget.plotDataItems.
    
    OBSOLETE:    
    Data loaded in the Working Data tree are stored in list workingDataTree.data. Each item in 
    the tree has a property item.dataIndex that is the position of the item's data in the list.
    
    To keep track of data plotted in dataPlotsWidget, the indexes of the plotted data are stored 
    in dataPlotsWidget.plotDataIndex
    """
    
    def __init__(self, parent=None):    
        # Initialise and setup UI
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        
        # Lists for storing data
        self.db = None
        self.wdb = None
        
        # Current working file and folder for saving
        self.currentSaveFile = []
        self.currentFolder = self.ui.dirTree.homeFolder
        self.saveFolder = self.currentFolder

        # Share instance with other modules by setting global variable browser
        utilsconsole.set_browser(self)

        # Load custom analysis modules
        self.customToolSelector  = toolselector.ToolSelector()        
        for module in dir(moduleLoader):               
            try:    
                sys.modules['analysis.modules.'+module].AnalysisModule(self)
                #print dir(m)
                #if hasattr(m, 'AnalysisModule'): 
                #    m.AnalysisModule(self)   
                #    print 'Loaded module', m
            except KeyError:
                pass
            except:    
                print module, sys.exc_info()


        # Directory browser
        # -----------------------------------------------------------------------------
        self.ui.dirTree.selectionModel().selectionChanged.connect(self.load_h5_OnSelectionChanged)
        self.ui.loadFolderInput.setText(self.currentFolder)
        self.ui.loadFolderButton.clicked.connect(self.select_loadFolder)
        self.ui.saveFolderInput.setText(self.currentFolder)
        self.ui.saveFolderButton.clicked.connect(self.select_saveFolder)

        # File data tree
        # -----------------------------------------------------------------------------
        self.ui.fileDataTree.data = []
        self.ui.fileDataTree.currentItemChanged.connect(self.plot_OnSelectionChanged)
        self.ui.fileDataTree.itemSelectionChanged.connect(lambda: self.store_Selection(1))
        self.ui.workingDataTree.itemSelectionChanged.connect(lambda: self.store_Selection(2))
        self.ui.loadFolderInput.returnPressed.connect(self.update_loadDir)
        self.ui.saveFolderInput.textChanged.connect(self.update_saveDir)

        # Analysis selection list
        # -----------------------------------------------------------------------------
        self.ui.oneDimToolSelect.selectionModel().selectionChanged.connect(self.select_analysisTool)
        self.ui.customToolSelect.selectionModel().selectionChanged.connect(self.select_analysisTool)
        self.ui.behaviourToolSelect.selectionModel().selectionChanged.connect(self.select_analysisTool)
        self.ui.graphToolSelect.selectionModel().selectionChanged.connect(self.select_analysisTool)
        self.ui.imageToolSelect.selectionModel().selectionChanged.connect(self.select_analysisTool)                
        self.selectionList = []
        self.selectionList.append([self.ui.oneDimToolSelect, self.ui.oneDimToolStackedWidget, '1D Analysis'])
        self.selectionList.append([self.ui.behaviourToolSelect, self.ui.behaviourToolStackedWidget, 'Behaviour Analysis'])
        self.selectionList.append([self.ui.imageToolSelect, self.ui.imageToolStackedWidget, 'Image Analysis'])
        self.selectionList.append([self.ui.graphToolSelect, self.ui.graphToolStackedWidget, 'Graph'])        
        self.selectionList.append([self.ui.customToolSelect, self.ui.customToolStackedWidget, 'Custom Analysis'])

        # Analysis tools stack
        # -----------------------------------------------------------------------------
        #self.ui.oneDimToolStackedWidget.eventCutOut.clicked.connect(self.event_cutOut)
        #self.ui.oneDimToolStackedWidget.eventThreshold.toggled.connect(self.event_showThresholdCursor)        

        # Working data tree
        # -----------------------------------------------------------------------------
        self.ui.workingDataTree.data = []
        self.ui.workingDataTree.dataItems = []
        self.ui.workingDataTree.root = self.ui.workingDataTree.invisibleRootItem()
        self.ui.workingDataTree.root.attrs = {}
        self.ui.actionLoadData.triggered.connect(self.load_h5OnLoadPush)
        self.ui.actionNewFile.triggered.connect(self.create_h5OnNewPush)
        self.ui.actionSaveFile.triggered.connect(self.save_h5OnSavePush)
        self.ui.actionSaveFileAs.triggered.connect(self.save_h5OnSaveAsPush)
        self.connect(self.ui.workingDataTree, QtCore.SIGNAL('dropped'), self.move_itemsAcross)
        self.connect(self.ui.workingDataTree, QtCore.SIGNAL('targetPosition'), self.set_targetPosition)
        self.connect(self.ui.workingDataTree, QtCore.SIGNAL('deletePressed'), self.remove_itemOnMenu)
        self.ui.workingDataTree.currentItemChanged.connect(self.browse_OnSelectionChanged)
        self.ui.workingDataTree.propsDt = ''
        self.ui.workingDataTree.propsDescription = ''   

        # Context menu
        self.ui.workingDataTree.customContextMenuRequested.connect(self.open_workingDataTreeMenu)
        self.ui.actionAddRootGroup.triggered.connect(self.add_rootGroupOnMenu)
        self.ui.actionAddChildGroup.triggered.connect(self.add_childGroupOnMenu)
        self.ui.actionRenameTreeItem.triggered.connect(self.rename_itemOnMenu)
        self.ui.actionRemoveTreeItem.triggered.connect(self.remove_itemOnMenu)
        self.ui.actionShowInTable.triggered.connect(self.show_inTableOnMenu)    

        # Data table        
        # -----------------------------------------------------------------------------
        self.connect(self.ui.dataTableWidget, QtCore.SIGNAL('droppedInTable'), self.copy_itemsToTable)
        self.connect(self.ui.dataTableWidget, QtCore.SIGNAL('tableTargetPosition'), self.set_targetTablePosition)

        # Properties table        
        # -----------------------------------------------------------------------------        
        self.ui.propsTableWidget.setRowCount(1)
        self.ui.propsTableWidget.setColumnCount(1)
        self.ui.propsTableWidget.horizontalHeader().setVisible(False)
        self.ui.propsTableWidget.setData({'dt':['']})
        #self.ui.workingDataTree.propsItemDtLabel = QtGui.QTableWidgetItem('dt')
        #self.ui.workingDataTree.propsItemDt = QtGui.QTableWidgetItem(self.ui.workingDataTree.propsDt)
        #self.ui.workingDataTree.propsItemDescriptionLabel = QtGui.QTableWidgetItem('Description')
        #self.ui.workingDataTree.propsItemDescription = QtGui.QTableWidgetItem(self.ui.workingDataTree.propsDescription)                
        #self.ui.propsTableWidget.setVerticalHeaderItem(0, self.ui.workingDataTree.propsItemDtLabel)
        #self.ui.propsTableWidget.setItem(0,0,self.ui.workingDataTree.propsItemDt)
        #self.ui.propsTableWidget.setVerticalHeaderItem(1, self.ui.workingDataTree.propsItemDescriptionLabel)
        #self.ui.propsTableWidget.setItem(1,0,self.ui.workingDataTree.propsItemDescription)
        #self.connect(self.ui.propsTableWidget, QtCore.SIGNAL('updateAttr'), self.updateItemAttrs)     
        self.ui.propsTableWidget.itemSelectionChanged.connect(self.updateItemAttrs)        

        
        # IPython tab
        # -----------------------------------------------------------------------------        
        self.ui.IPythonWidget.pushVariables({'browser': self, 'aux': auxfuncs, 'dataTree': self.ui.workingDataTree,
                                    'dataPlot': self.ui.dataPlotsWidget, 'ndaq': utilsconsole, 
                                    'canvas': self.ui.mplWidget.canvas, 'ax': self.ui.mplWidget.canvas.ax})

        # Plots tab
        # ----------------------------------------------------------------------------- 
        self.ui.actionPlotData.triggered.connect(self.plot_selected)
        self.ui.actionShowCursors.triggered.connect(self.show_cursors)
        self.ui.actionAnalyseData.triggered.connect(self.analyse_data)



    # -----------------------------------------------------------------------------
    # HDF5 file Methods
    # -----------------------------------------------------------------------------
    def load_h5_OnSelectionChanged(self, newSelection, oldSelection):
        """ Load hdf5 file
        """
        if self.db: 
            if self.dbType=='hdf5':
                self.db.close()
            self.db = None
        h5.load_h5(self, self.ui.fileDataTree, push=False)

    def load_h5OnLoadPush(self):
        h5.load_h5(self, self.ui.workingDataTree, push=True)
        
    def create_h5OnNewPush(self):
        h5.create_h5(self, self.ui.workingDataTree)

    def save_h5OnSavePush(self):
        if self.currentSaveFile:
            fname = os.path.split(self.currentSaveFile)[1] # update save folder to user selected if necessary
            self.currentSaveFile = str(self.saveFolder) + '/' + fname
            h5.save_h5(self, self.ui.workingDataTree)
        else: 
            fname, ok = QtGui.QInputDialog.getText(self, 'New file', 'Enter file name:')
            if ok:
                self.currentSaveFile = str(self.saveFolder) + '/' + fname + '.hdf5'
                h5.save_h5(self, self.ui.workingDataTree)
        
    def save_h5OnSaveAsPush(self):
        fname, ok = QtGui.QInputDialog.getText(self, 'New file', 'Enter file name:')
        if self.ui.saveFolderInput.text()<>'': self.update_saveDir()
        if ok:
            self.currentSaveFile = self.saveFolder + '/' + fname + '.hdf5'      
            h5.save_h5(self, self.ui.workingDataTree)        


    # -----------------------------------------------------------------------------
    # Tree Methods
    # -----------------------------------------------------------------------------    
    def update_loadDir(self):
        treefun.set_loadFolder(self, self.ui.dirTree, self.ui.loadFolderInput.text())

    def update_saveDir(self):
        self.saveFolder = self.ui.saveFolderInput.text()

    def select_loadFolder(self):
        folder = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Folder", self.currentFolder))
        treefun.set_loadFolder(self, self.ui.dirTree, folder)
        self.ui.loadFolderInput.setText(folder)

    def select_saveFolder(self):
        self.saveFolder = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Folder", self.saveFolder))        
        self.ui.saveFolderInput.setText(self.saveFolder)
    
    def store_Selection(self, source):
        """ Store user selected tree items in dragItems list to get them back
        once they have been dropped. Source '1' is fileDataTree and '2' is
        workingDataTree. 
        """
        if source==1:   # Move
            self.dragItems = []
            dataTree = self.ui.fileDataTree
            for originalIndex in dataTree.selectedIndexes():
                item = dataTree.itemFromIndex(QtCore.QModelIndex(originalIndex))
                self.dragItems.append([item.path, item.text(0), item.listIndex, originalIndex])
        elif source==2: # Copy
            dataTree = self.ui.workingDataTree
            self.copyItems = []
            for item in self.ui.workingDataTree.selectedItems():          
                self.copyItems.append(item)        

    def move_itemsAcross(self, source, modifiers):
        """ Create new tree items and populate the target tree. Originally made 
        for moving items from fileDataTree to workingDataTree, but then modified
        to copy items when the move is internal in workingDataTree and Ctrl is 
        pressed.
        """
        if (source==self.ui.workingDataTree) and (modifiers==QtCore.Qt.ControlModifier):
          # Copy internally
          #print 'copying'
          targetItems = []
          for item in self.copyItems:
            i = h5Item([str(item.text(0))])
            i.data = item.data
            targetItems.append(i)             
          parentIndex = self.ui.workingDataTree.indexFromItem(self.dragTargetParent)
          for row in np.arange(0, len(self.copyItems)):
            index = self.ui.workingDataTree.model().index(self.dragTargetRow+row, 0, parentIndex)        
            temp_item = self.ui.workingDataTree.itemFromIndex(QtCore.QModelIndex(index))
            sip.delete(temp_item)        
            if parentIndex.isValid():
                self.make_nameUnique(self.dragTargetParent, targetItems[row], targetItems[row].text(0))
                self.dragTargetParent.insertChild(index.row(), targetItems[row])
                originalParentWidget = self.copyItems[row]
                h5.populate_h5copyItems(self, originalParentWidget, targetItems[row])
            else:
                self.make_nameUnique(self.ui.workingDataTree.invisibleRootItem(), targetItems[row], targetItems[row].text(0))
                self.ui.workingDataTree.insertTopLevelItem(index.row(), targetItems[row])     
                originalParentWidget = self.copyItems[row]
                h5.populate_h5copyItems(self, originalParentWidget, targetItems[row])       
        elif source==self.ui.workingDataTree:
          pass
        else:
          # Move across
          #print 'moving'
          targetItems = []
          for item in self.dragItems:
            i = h5Item([str(item[1])])
            i.path = item[0]
            i.listIndex = item[2]
            i.originalIndex = item[3]
            targetItems.append(i)             
          parentIndex = self.ui.workingDataTree.indexFromItem(self.dragTargetParent)
          for row in np.arange(0, len(self.dragItems)):
            index = self.ui.workingDataTree.model().index(self.dragTargetRow+row, 0, parentIndex)        
            temp_item = self.ui.workingDataTree.itemFromIndex(QtCore.QModelIndex(index))
            sip.delete(temp_item)        
            if parentIndex.isValid():
                self.make_nameUnique(self.dragTargetParent, targetItems[row], targetItems[row].text(0))
                self.dragTargetParent.insertChild(index.row(), targetItems[row])
                originalParentWidget = self.ui.fileDataTree.itemFromIndex(QtCore.QModelIndex(targetItems[row].originalIndex))
                h5.populate_h5dragItems(self, originalParentWidget, targetItems[row])
            else:
                self.make_nameUnique(self.ui.workingDataTree.invisibleRootItem(), targetItems[row], targetItems[row].text(0))
                self.ui.workingDataTree.insertTopLevelItem(index.row(), targetItems[row])     
                originalParentWidget = self.ui.fileDataTree.itemFromIndex(QtCore.QModelIndex(targetItems[row].originalIndex))
                h5.populate_h5dragItems(self, originalParentWidget, targetItems[row])
                
    def set_targetPosition(self, parent, row):
        self.dragTargetParent = parent
        self.dragTargetRow = row

    def make_nameUnique(self, parentWidget, item, originalName):
        """ Check existing names in parentWidget that start with item.text
        and get the next available index, as item.text_index.
        Updates item.text if name is not unique.
        """
        names = []
        name = originalName
        if parentWidget.childCount()>0:
            for c in range(parentWidget.childCount()):
                child = parentWidget.child(c)
                names.append(str(child.text(0)))
            unique = False
            i = 1
            while not unique:
                if name in names:
                    name = originalName + '_' + str(i)
                    i+=1
                else:
                    unique = True
        item.setText(0, name)

    def open_workingDataTreeMenu(self, position):
        """ Context menu for working data tree
        """
        self.workingDataTreeMenu = QtGui.QMenu()
        self.workingDataTreeMenu.addAction(self.ui.actionAddRootGroup)
        self.workingDataTreeMenu.addAction(self.ui.actionAddChildGroup)
        self.workingDataTreeMenu.addAction(self.ui.actionAddDataset)
        self.workingDataTreeMenu.addSeparator()
        self.workingDataTreeMenu.addAction(self.ui.actionRenameTreeItem)
        self.workingDataTreeMenu.addAction(self.ui.actionShowInTable)
        self.workingDataTreeMenu.addAction(self.ui.actionRemoveTreeItem)

        if len(self.ui.workingDataTree.selectedItems())==0: 
            self.ui.actionAddChildGroup.setDisabled(True)
            self.ui.actionRenameTreeItem.setDisabled(True)
        else:
            self.ui.actionAddChildGroup.setDisabled(False)
            self.ui.actionRenameTreeItem.setDisabled(False)            
        self.workingDataTreeMenu.exec_(self.ui.workingDataTree.viewport().mapToGlobal(position))

    def add_rootGroupOnMenu(self):
        text, ok = QtGui.QInputDialog.getText(self, 'New root group', 'Enter name:')
        if ok: treefun.add_treeGroup(self, self.ui.workingDataTree, 'root', str(text))
       
    def add_childGroupOnMenu(self):
        text, ok = QtGui.QInputDialog.getText(self, 'New child group', 'Enter name:')
        if ok: treefun.add_treeGroup(self, self.ui.workingDataTree, 'child', str(text))
    
    def rename_itemOnMenu(self):        
        currentText = self.ui.workingDataTree.currentItem().text(0)
        text, ok = QtGui.QInputDialog.getText(self, 'Rename item', 'Enter new name:', text=currentText)
        if ok: treefun.rename_treeItem(self, self.ui.workingDataTree, str(text))

    def remove_itemOnMenu(self):
        treefun.remove_treeItem(self, self.ui.workingDataTree)

    def show_inTableOnMenu(self):
        table.clear_table(self)
        table.put_dataOnTable(self)

    # -----------------------------------------------------------------------------
    # Analysis Methods
    # -----------------------------------------------------------------------------
    def select_analysisTool(self):
        i = self.ui.selectionTabWidget.currentIndex()
        for item in self.selectionList:
            if item[2]==self.ui.selectionTabWidget.tabText(i):  # get the widgets that belong to the selected tab
                toolSelectWidget = item[0]
                toolStackedWidget = item[1]                
        index = toolSelectWidget.selectedIndexes()[0]
    
        # Display the matching stack in the stacked widget
        selectedItemName = toolSelectWidget.model.itemFromIndex(index).text()
        for w in toolStackedWidget.widgetList:
            if w[0]==selectedItemName: toolStackedWidget.setCurrentIndex(w[1])
        return index        

    def analyse_data(self):
        index = self.select_analysisTool()
        if index:
            tool = index.data() #.toString()
            #toolselector.toolselector(self, tool)
            self.customToolSelector.tool_select(self, tool)

    # -----------------------------------------------------------------------------
    # Properties Methods
    # -----------------------------------------------------------------------------
    def updateItemAttrs(self):
        itemList = self.ui.workingDataTree.selectedItems()
        for item in itemList:
            attr = str(self.ui.propsTableWidget.verticalHeaderItem(0).text())
            #attrValue = float(self.ui.propsTableWidget.item(self.ui.propsTableWidget.currentItem().row(), 0).text()) # for dt
            attrValue = float(self.ui.propsTableWidget.currentItem().text())
            item.attrs[attr] = attrValue

    def test(self):
        print self.ui.propsTableWidget.currentItem().text()

    # -----------------------------------------------------------------------------
    # Table Methods
    # -----------------------------------------------------------------------------
    def show_inTableOnMenu(self):
        #self.ui.dataTableWidget.setData({'x': [1,2,3], 'y': [4,5,6]})#np.random.random(100))
        table.put_dataOnTable(self, self.ui.dataTableWidget)

    def set_targetTablePosition(self, col, row):
        self.dragTableTargetCol = col
        self.dragTableTargetRow = row

    def copy_itemsToTable(self, source, modifiers):
        if (source==self.ui.workingDataTree):
          print "something arrived at the Table"
          copyItems = []
          for item in self.copyItems:
             i = tableItem(str(item.text(0)))
             i.data = item.data
             targetItems.append(i)      
                 
          #parentIndex = self.ui.workingDataTree.indexFromItem(self.dragTargetParent)
          for row in np.arange(0, len(self.copyItems)):
             index = self.ui.dataTable.model().index(self.dragTableTargetCol, self.dragTableTargetRow) #, 0, parentIndex)        
             temp_item = self.ui.dataTable.itemFromIndex(QtCore.QModelIndex(index))
             sip.delete(temp_item)        
          #  if parentIndex.isValid():
          #      self.make_nameUnique(self.dragTargetParent, targetItems[row], targetItems[row].text(0))
          #      self.dragTargetParent.insertChild(index.row(), targetItems[row])
          #      originalParentWidget = self.copyItems[row]
          #      h5.populate_h5copyItems(self, originalParentWidget, targetItems[row])
          #  else:
          #      self.make_nameUnique(self.ui.workingDataTree.invisibleRootItem(), targetItems[row], targetItems[row].text(0))
          #      self.ui.workingDataTree.insertTopLevelItem(index.row(), targetItems[row])     
          #      originalParentWidget = self.copyItems[row]
          #      h5.populate_h5copyItems(self, originalParentWidget, targetItems[row])       


    # -----------------------------------------------------------------------------
    # Plotting Methods
    # -----------------------------------------------------------------------------
    def plot_OnSelectionChanged(self, current, previous):
        if current:
            data = h5.get_dataFromFile(self, current)
            if data is not None:
                pgplot.plot_singleData(self, self.ui.singlePlotWidget, data)    

    def browse_OnSelectionChanged(self, current, previous):
        if hasattr(current, 'data'): 
            # Show data values in status bar
            if current.data is not None:
                dataValue = str(current.data[0])
                self.ui.statusbar.showMessage('First data point value: ' + dataValue)
            else:
                self.ui.statusbar.clearMessage()
            # Plot data if Browse is selected
            if self.ui.actionBrowseData.isChecked():
              if current.data is not None: 
                if len(current.data.shape)==1:
                    pgplot.browse_singleData(self, self.ui.dataPlotsWidget, current)
                elif len(current.data.shape)==2:
                    pgplot.browse_image(self, self.ui.dataImageWidget, current)
            # Show dt
            self.ui.propsTableWidget.setData({'dt':[current.attrs['dt']]})

    def plot_selected(self):
        self.ui.actionBrowseData.setChecked(False)
        itemList = self.ui.workingDataTree.selectedItems()
        if itemList:
            pgplot.plot_multipleData(self, self.ui.dataPlotsWidget, itemList)   
            print itemList[0].attrs['dt']    

    def zoom_out(self):
        pgplot.zoom_out(self, self.ui.dataPlotsWidget)

    def show_cursors(self):
        if self.ui.actionShowCursors.isChecked():
            pgplot.show_cursors(self, self.ui.dataPlotsWidget)
            self.ui.dataPlotsWidget.cursor = True
        else:
            pgplot.hide_cursors(self, self.ui.dataPlotsWidget)
            self.ui.dataPlotsWidget.cursor = False

def main():    
    #defaultFont = QtGui.QFont('Ubuntu', 8) 
    app = QtGui.QApplication(sys.argv)
    #app.setFont(defaultFont)    
    browser = NeuroDaqWindow()
    sys.exit(app.exec_())
    return browser

if __name__ == '__main__':
    main() 





