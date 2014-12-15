# -*- coding: utf-8 -*-

import os
from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.qt.inprocess import QtInProcessKernelManager
from IPython.lib import guisupport

from PyQt4 import QtCore, QtGui
from widgets import *
import pyqtgraph as pg
import vlc


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_MainWindow(object):

    """ User interface main window for NeuroDAQ.
    Creates all the widgets and organizes geometry and layouts
    """

    def setupUi(self, MainWindow):
    
        """ Initialises the main window user interface
        """

        # Size policies
        preferredSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        expandingSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)


        # -----------------------------------------------------------------------------
        # Central Widget
        # -----------------------------------------------------------------------------

        # Geometry and Layout
        MainWindow.resize(1300, 780)                
        MainWindow.setSizePolicy(preferredSizePolicy)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(MainWindow)           
        self.gridLayout_centralwidget = QtGui.QGridLayout(self.centralwidget)
        self.splitter_centralwidget = QtGui.QSplitter(self.centralwidget)
        self.splitter_centralwidget.setOrientation(QtCore.Qt.Horizontal)
        self.gridLayout_centralwidget.addWidget(self.splitter_centralwidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle('NeuroDAQ Analysis')

        # -----------------------------------------------------------------------------
        # Left pane -> SelectionTabs Widget and SinglePlot Widget
        # -----------------------------------------------------------------------------
        # Geometry and Layout
        self.splitter_leftPane = QtGui.QSplitter(self.splitter_centralwidget)
        self.splitter_leftPane.setOrientation(QtCore.Qt.Vertical)


        # SelectionTabs Widget
        # -----------------------------------------------------------------------------
        # Geometry and Layout             
        self.selectionTabWidget = TabWidget(0,500)       
        self.selectionTabWidget.setSizePolicy(preferredSizePolicy)
        self.selectionTabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.selectionTabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.selectionTabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.splitter_leftPane.addWidget(self.selectionTabWidget)

        # ------
        # TAB 1   (DataTab) -> dirTree and fileDataTree
        # ------
        # Geometry and Layout        
        self.dataTab = NeuroWidget(0,0)
        self.selectionTabWidget.addTab(self.dataTab, _fromUtf8("Data"))        
        self.gridLayout_dataTab = QtGui.QGridLayout(self.dataTab)
        self.verticalsplitter_dataTab = QtGui.QSplitter(self.dataTab)
        self.verticalsplitter_dataTab.setSizePolicy(preferredSizePolicy)
        self.verticalsplitter_dataTab.setOrientation(QtCore.Qt.Vertical)        
        self.verticalsplitter_dataTab_layout = QtGui.QGridLayout(self.verticalsplitter_dataTab)

        # TAB 1 content > Folder input
        self.dataFolderWidget = NeuroWidget(0,0, parent=self.verticalsplitter_dataTab)
        self.folderLayout = QtGui.QGridLayout(self.dataFolderWidget)
        self.loadFolderInput = QtGui.QLineEdit()
        self.loadFolderLabel = QtGui.QLabel('Load')
        self.folderLayout.addWidget(self.loadFolderInput, 0, 0)
        self.folderLayout.addWidget(self.loadFolderLabel, 0, 1)
        self.saveFolderInput = QtGui.QLineEdit()
        self.saveFolderLabel = QtGui.QLabel('Save')
        self.folderLayout.addWidget(self.saveFolderInput, 1, 0)
        self.folderLayout.addWidget(self.saveFolderLabel, 1, 1)
        
               
        # TAB 1 content > DirTree
        self.horizontalsplitter_dataTab = QtGui.QSplitter(self.verticalsplitter_dataTab)
        self.horizontalsplitter_dataTab.setSizePolicy(preferredSizePolicy)
        self.horizontalsplitter_dataTab.setOrientation(QtCore.Qt.Horizontal)                
        self.gridLayout_dataTab.addWidget(self.verticalsplitter_dataTab, 0, 0, 1, 1)
        self.dirTree = FileBrowserWidget(0,0) #, homeFolder = '/home/tiago/Code/py/NeuroDAQanalysis/testData/')
        self.horizontalsplitter_dataTab.addWidget(self.dirTree)
        self.dirTree.setSizePolicy(preferredSizePolicy)
        
        # TAB 1 content > FileDataTree
        self.fileDataTree = h5TreeWidget(0,0)
        self.horizontalsplitter_dataTab.addWidget(self.fileDataTree)
        self.fileDataTree.setSizePolicy(preferredSizePolicy)
        self.fileDataTree.setAcceptDrops(True)
        self.fileDataTree.setDragEnabled(True)
        self.fileDataTree.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.fileDataTree.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.fileDataTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.fileDataTree.setSortingEnabled(True)
        self.fileDataTree.headerItem().setText(0, _fromUtf8("Data"))

        self.verticalsplitter_dataTab.setSizes([1,500])
        
        # -----
        # TAB 2   (oneDimAnalysisTab) -> toolSelect and toolStackedWidget
        # -----
        # Geometry and Layout
        self.oneDimAnalysisTab = NeuroWidget(0,0)
        self.selectionTabWidget.addTab(self.oneDimAnalysisTab, _fromUtf8("1D Analysis"))
        self.gridLayout_oneDimAnalysisTab = QtGui.QGridLayout(self.oneDimAnalysisTab)
        self.splitter_oneDimAnalysisTab = QtGui.QSplitter(self.oneDimAnalysisTab)
        self.splitter_oneDimAnalysisTab.setSizePolicy(preferredSizePolicy)        
        self.splitter_oneDimAnalysisTab.setOrientation(QtCore.Qt.Horizontal)
        self.gridLayout_oneDimAnalysisTab.addWidget(self.splitter_oneDimAnalysisTab, 0, 0, 1, 1)

        # TAB 2 content > Tool Select        
        self.oneDimToolSelect = AnalysisSelectWidget(0,0)
        self.splitter_oneDimAnalysisTab.addWidget(self.oneDimToolSelect)
        self.oneDimToolSelect.setSizePolicy(preferredSizePolicy)
        

        # TAB 2 content > Tools Stacked Widget    
        self.toolStackContainerWidget = NeuroWidget(0,0)   
        self.toolStackGrid = QtGui.QGridLayout(self.toolStackContainerWidget)
        self.splitter_oneDimAnalysisTab.addWidget(self.toolStackContainerWidget)
        self.toolDataSourceBox = QtGui.QComboBox()
        self.toolDataSourceBox.addItem("Plot")
        self.toolDataSourceBox.addItem("Selection")   
        self.toolStackGrid.addWidget(self.toolDataSourceBox)
        self.oneDimToolStackedWidget = AnalysisStackWidget(0,0)
        self.toolStackGrid.addWidget(self.oneDimToolStackedWidget)
        self.oneDimToolStackedWidget.setSizePolicy(preferredSizePolicy)        
        
        # -----
        # TAB 3   (behaviourAnalysisTab) -> toolSelect and toolStackedWidget
        # -----
        # Geometry and Layout
        self.behaviourAnalysisTab = NeuroWidget(0,0)
        self.selectionTabWidget.addTab(self.behaviourAnalysisTab, _fromUtf8("Behaviour Analysis"))
        self.gridLayout_behaviourAnalysisTab = QtGui.QGridLayout(self.behaviourAnalysisTab)
        self.splitter_behaviourAnalysisTab = QtGui.QSplitter(self.behaviourAnalysisTab)
        self.splitter_behaviourAnalysisTab.setSizePolicy(preferredSizePolicy)        
        self.splitter_behaviourAnalysisTab.setOrientation(QtCore.Qt.Horizontal)
        self.gridLayout_behaviourAnalysisTab.addWidget(self.splitter_behaviourAnalysisTab, 0, 0, 1, 1)

        # TAB 2 content > Tool Select        
        self.behaviourToolSelect = AnalysisSelectWidget(0,0)
        self.splitter_behaviourAnalysisTab.addWidget(self.behaviourToolSelect)
        self.behaviourToolSelect.setSizePolicy(preferredSizePolicy)
        

        # TAB 2 content > Tools Stacked Widget    
        self.behaviourToolStackContainerWidget = NeuroWidget(0,0)   
        self.behaviourToolStackGrid = QtGui.QGridLayout(self.behaviourToolStackContainerWidget)
        self.splitter_behaviourAnalysisTab.addWidget(self.behaviourToolStackContainerWidget)
        self.behaviourToolDataSourceBox = QtGui.QComboBox()
        self.behaviourToolDataSourceBox.addItem("Plot")
        self.behaviourToolDataSourceBox.addItem("Selection")   
        self.behaviourToolStackGrid.addWidget(self.behaviourToolDataSourceBox)
        self.behaviourToolStackedWidget = AnalysisStackWidget(0,0)
        self.behaviourToolStackGrid.addWidget(self.behaviourToolStackedWidget)
        self.behaviourToolStackedWidget.setSizePolicy(preferredSizePolicy)        
        

        # -----
        # TAB 4   (customAnalysisTab) -> toolSelect and toolStackedWidget
        # -----
        # Geometry and Layout
        self.customAnalysisTab = NeuroWidget(0,0)
        self.selectionTabWidget.addTab(self.customAnalysisTab, _fromUtf8("Custom Analysis"))
        self.gridLayout_customAnalysisTab = QtGui.QGridLayout(self.customAnalysisTab)
        self.splitter_customAnalysisTab = QtGui.QSplitter(self.customAnalysisTab)
        self.splitter_customAnalysisTab.setSizePolicy(preferredSizePolicy)        
        self.splitter_customAnalysisTab.setOrientation(QtCore.Qt.Horizontal)
        self.gridLayout_customAnalysisTab.addWidget(self.splitter_customAnalysisTab, 0, 0, 1, 1)

        # TAB 3 content > Tool Select        
        self.customToolSelect = AnalysisSelectWidget(0,0)
        self.splitter_customAnalysisTab.addWidget(self.customToolSelect)
        self.customToolSelect.setSizePolicy(preferredSizePolicy)
        

        # TAB 3 content > Tools Stacked Widget    
        self.customToolStackContainerWidget = NeuroWidget(0,0)   
        self.customToolStackGrid = QtGui.QGridLayout(self.customToolStackContainerWidget)
        self.splitter_customAnalysisTab.addWidget(self.customToolStackContainerWidget)
        self.customToolDataSourceBox = QtGui.QComboBox()
        self.customToolDataSourceBox.addItem("Plot")
        self.customToolDataSourceBox.addItem("Selection")   
        self.customToolStackGrid.addWidget(self.customToolDataSourceBox)
        self.customToolStackedWidget = AnalysisStackWidget(0,0)
        self.customToolStackGrid.addWidget(self.customToolStackedWidget)
        self.customToolStackedWidget.setSizePolicy(preferredSizePolicy) 
        

        # SinglePlots Widget
        # -----------------------------------------------------------------------------       
        # Geometry and Layout 
        #self.singlePlotWidget = matplotlibWidget(0,200)
        self.singlePlotWidget = pg.PlotWidget(background='#ECEDEB')
        self.singlePlotWidget.getAxis('bottom').setPen('k')
        self.singlePlotWidget.getAxis('left').setPen('k')           
        self.splitter_leftPane.addWidget(self.singlePlotWidget)
        self.singlePlotWidget.setSizePolicy(preferredSizePolicy)

        self.splitter_leftPane.setSizes([300,1])


        # -----------------------------------------------------------------------------
        # Middle pane -> DisplayTabs Widget 
        # -----------------------------------------------------------------------------        
          
        # DisplayTabs Widget
        # -----------------------------------------------------------------------------
        # Geometry and Layout
        self.displayTabWidget = TabWidget(0,0)
        self.displayTabWidget.setSizePolicy(preferredSizePolicy)
        self.splitter_centralwidget.addWidget(self.displayTabWidget)
    

        # ------
        # TAB 1   (PlotTab)
        # ------    
        # Geometry and Layout
        self.dataPlotsTab = NeuroWidget(0,0)
        self.displayTabWidget.addTab(self.dataPlotsTab, 'Plot')
        self.gridLayout_plots = QtGui.QGridLayout(self.dataPlotsTab)
         
        # TAB 1 content > dataPlotsWidget        
        #self.dataPlotsWidget = matplotlibWidget(0,0)
        self.dataPlotsWidget = pg.PlotWidget(background='#ECEDEB')
        self.dataPlotsWidget.getAxis('bottom').setPen('k')
        self.dataPlotsWidget.getAxis('left').setPen('k')        
        self.dataPlotsWidget.showGrid(x=True, y=True, alpha=0.3)
        self.dataPlotsWidget.setSizePolicy(preferredSizePolicy)
        self.gridLayout_plots.addWidget(self.dataPlotsWidget)
        # Cursors     
        self.dataPlotsWidget.cursor1 = pg.InfiniteLine(angle=90, movable=True,
                                      pen=pg.mkPen('#2AB825', width=2, style=QtCore.Qt.DotLine))
        self.dataPlotsWidget.cursor2 = pg.InfiniteLine(angle=90, movable=True, 
                                      pen=pg.mkPen('#2AB825', width=2, style=QtCore.Qt.DotLine))           
        self.dataPlotsWidget.cursor = False
        # Toolbar
        self.plotToolBar = QtGui.QToolBar()
        self.plotToolBar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.gridLayout_plots.addWidget(self.plotToolBar)       
        
        
        # ------
        # TAB 2   (TableTab)
        # ------        
        # Geometry and Layout   
        # TAB 2 content > tableWidget         
        #self.dataTableWidget = QtGui.QTableWidget()
        self.dataTableWidget = pg.TableWidget(editable=False)
        self.dataTableWidget.setAlternatingRowColors(True)
        self.dataTableWidget.setColumnCount(100)
        self.dataTableWidget.setRowCount(100)
        self.displayTabWidget.addTab(self.dataTableWidget, _fromUtf8("Table"))        

        # ------
        # TAB 3   (IPythonTab)
        # ------        
        # Geometry and Layout   
        # TAB 3 content > IPython console         
        self.IPythonWidget = QIPythonWidget()
        self.displayTabWidget.addTab(self.IPythonWidget, _fromUtf8("IPython"))        

        # ------
        # TAB 4   (Matplotlib Tab)
        # ------        
        # Geometry and Layout   
        # TAB 4 content > Matplotlib axes
        self.mplWidget = matplotlibWidget()
        self.displayTabWidget.addTab(self.mplWidget, _fromUtf8("MatplotLib"))


        # ------
        # TAB 5   (Notes Tab)
        # ------        
        # Geometry and Layout   
        # TAB 5 content > Notes text edit
        self.notesWidget = QtGui.QTextEdit()
        self.displayTabWidget.addTab(self.notesWidget, _fromUtf8("Notes"))


        # -----------------------------------------------------------------------------
        # Right pane -> Working Data Tree and Properties Table
        # -----------------------------------------------------------------------------
        # Geometry and Layout      
        self.splitter_rightPane = QtGui.QSplitter(self.splitter_centralwidget)
        self.splitter_rightPane.setSizePolicy(preferredSizePolicy)
        self.splitter_rightPane.setOrientation(QtCore.Qt.Vertical)
        
        # WorkingDataTree Widget
        # -----------------------------------------------------------------------------        
        self.workingDataTree = h5TreeWidget(0,0)
        self.splitter_rightPane.addWidget(self.workingDataTree)
        self.workingDataTree.setSizePolicy(preferredSizePolicy)
        self.workingDataTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workingDataTree.setAcceptDrops(True)
        self.workingDataTree.setDragEnabled(True)
        self.workingDataTree.setDropIndicatorShown(True)
        #self.workingDataTree.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        #self.workingDataTree.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.workingDataTree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.workingDataTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.workingDataTree.headerItem().setText(0, _fromUtf8("Working Data"))
        
        # Properties Table Widget
        # -----------------------------------------------------------------------------
        #self.propsTableWidget = pg.TableWidget(self.splitter_rightPane, editable=True)
        self.propsTableWidget = TablePropsWidget(self.splitter_rightPane, editable=True)
        #self.propsTableWidget = QtGui.QTableWidget(self.splitter_rightPane)
        self.propsTableWidget.setSizePolicy(preferredSizePolicy)
        self.propsTableWidget.setRowCount(0)
        self.propsTableWidget.setColumnCount(0)
        self.propsTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.propsTableWidget.horizontalHeader().setStretchLastSection(True)
    
        self.splitter_centralwidget.setSizes([400,800,200])
        self.splitter_rightPane.setSizes([500,1])
        
        # -----------------------------------------------------------------------------
        # Status Bar
        # -----------------------------------------------------------------------------        
        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.setLayoutDirection(QtCore.Qt.RightToLeft)
        #self.statusbar.showMessage('Ready')
        
        # -----------------------------------------------------------------------------
        # ToolBars
        # -----------------------------------------------------------------------------
        # Top toolbar
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

 
        # -----------------------------------------------------------------------------
        # Actions
        # -----------------------------------------------------------------------------
        # Top Toolbar
        self.actionLoadData = QtGui.QAction('Load', MainWindow)
        self.actionNewFile = QtGui.QAction('New', MainWindow)
        self.actionSaveFile = QtGui.QAction('Save', MainWindow)       
        self.actionSaveFileAs = QtGui.QAction('Save As', MainWindow)        
        self.toolBar.addAction(self.actionNewFile)
        self.toolBar.addAction(self.actionLoadData)
        self.toolBar.addAction(self.actionSaveFile)
        self.toolBar.addAction(self.actionSaveFileAs)        

        # Plot Toolbar 
        self.actionPlotData = QtGui.QAction('Plot', MainWindow) 
        self.actionBrowseData = QtGui.QAction('Browse', MainWindow)
        self.actionBrowseData.setCheckable(True)         
        self.actionShowCursors = QtGui.QAction('Cursors', MainWindow)
        self.actionShowCursors.setCheckable(True)
        self.actionAnalyseData = QtGui.QAction('Analyse', MainWindow)
        self.plotToolBar.addAction(self.actionBrowseData)
        self.plotToolBar.addAction(self.actionPlotData)
        self.plotToolBar.addAction(self.actionShowCursors)
        self.plotToolBar.addAction(self.actionAnalyseData)
                
        # File data tree context menu        
        self.actionAddRootGroup = QtGui.QAction('Add Root Group', MainWindow)
        self.actionAddChildGroup = QtGui.QAction('Add Child Group', MainWindow)
        self.actionAddDataset = QtGui.QAction('Add Dataset', MainWindow)
        self.actionRenameTreeItem = QtGui.QAction('Rename', MainWindow)
        self.actionShowInTable = QtGui.QAction('Show in Table', MainWindow)
        self.actionRemoveTreeItem = QtGui.QAction('Remove', MainWindow)     
        
        
        
        
        
        
