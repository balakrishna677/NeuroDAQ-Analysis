# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from widgets import *
import pyqtgraph as pg

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

        # TAB 1 content > Folder input
        self.loadFolderInput = QtGui.QLineEdit(self.verticalsplitter_dataTab)
        self.loadFolderInput.setSizePolicy(preferredSizePolicy)
               
        # TAB 1 content > DirTree
        self.horizontalsplitter_dataTab = QtGui.QSplitter(self.verticalsplitter_dataTab)
        self.horizontalsplitter_dataTab.setSizePolicy(preferredSizePolicy)
        self.horizontalsplitter_dataTab.setOrientation(QtCore.Qt.Horizontal)                
        self.gridLayout_dataTab.addWidget(self.verticalsplitter_dataTab, 0, 0, 1, 1)
        self.dirTree = FileBrowserWidget(0,0)
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
        self.toolStackedWidget = AnalysisStackWidget(0,0)
        self.splitter_oneDimAnalysisTab.addWidget(self.toolStackedWidget)
        self.toolStackedWidget.setSizePolicy(preferredSizePolicy)
        
        # TOOLS in Stacked Widget
        # Averaging
        self.avgTool = NeuroWidget(0,0)
        self.checkBox = QtGui.QCheckBox(self.avgTool)
        self.checkBox.setGeometry(QtCore.QRect(10, 30, 97, 22))
        self.toolStackedWidget.addWidget(self.avgTool)
        self.avgTool.setSizePolicy(preferredSizePolicy)
        
        # Baseline  
        self.baselineTool = NeuroWidget(0,0)
        self.toolStackedWidget.addWidget(self.baselineTool)
        
        # Measure
        self.measureTool = NeuroWidget(0,0)
        self.toolStackedWidget.addWidget(self.measureTool)
        

        # SinglePlots Widget
        # -----------------------------------------------------------------------------       
        # Geometry and Layout 
        #self.singlePlotWidget = matplotlibWidget(0,200)
        self.singlePlotWidget = pg.PlotWidget(background='w')
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
        self.dataPlotsWidget = pg.PlotWidget(background='w')
        self.dataPlotsWidget.setSizePolicy(preferredSizePolicy)
        #self.displayTabWidget.addTab(self.dataPlotsWidget, _fromUtf8("Plot"))
        #self.cursor = pg.InfiniteLine(pos=0, angle=90, movable=True, pen=pg.mkPen('c', width=2))
        #self.dataPlotsWidget.addItem(self.cursor)
        self.gridLayout_plots.addWidget(self.dataPlotsWidget)
        # Toolbar
        self.plotToolBar = QtGui.QToolBar()
        self.plotToolBar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.gridLayout_plots.addWidget(self.plotToolBar)
        
        # ------
        # TAB 2   (TableTab)
        # ------        
        # Geometry and Layout   
        # TAB 2 content > tableWidget         
        self.dataTableWidget = QtGui.QTableWidget()
        self.dataTableWidget.setDragEnabled(True)
        self.dataTableWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.dataTableWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.dataTableWidget.setAlternatingRowColors(True)
        self.dataTableWidget.setColumnCount(0)
        self.dataTableWidget.setRowCount(0)
        self.displayTabWidget.addTab(self.dataTableWidget, _fromUtf8("Table"))        



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
        self.workingDataTree.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.workingDataTree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.workingDataTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.workingDataTree.headerItem().setText(0, _fromUtf8("Working Data"))
        
        # Properties Table Widget
        # -----------------------------------------------------------------------------
        self.propsTableWidget = QtGui.QTableWidget(self.splitter_rightPane)
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
        self.actionZoomOut = QtGui.QAction('Zoom Out', MainWindow)         
        self.actionShowCursors = QtGui.QAction('Cursors', MainWindow)
        self.actionAnalyseData = QtGui.QAction('Analyse', MainWindow)
        self.plotToolBar.addAction(self.actionPlotData)
        self.plotToolBar.addAction(self.actionZoomOut)
        self.plotToolBar.addAction(self.actionShowCursors)
        self.plotToolBar.addAction(self.actionAnalyseData)
                
        # File data tree context menu        
        self.actionAddRootGroup = QtGui.QAction('Add Root Group', MainWindow)
        self.actionAddChildGroup = QtGui.QAction('Add Child Group', MainWindow)
        self.actionAddDataset = QtGui.QAction('Add Dataset', MainWindow)
        self.actionRenameTreeItem = QtGui.QAction('Rename', MainWindow)
        self.actionRemoveTreeItem = QtGui.QAction('Remove', MainWindow)
        self.actionShowInTable = QtGui.QAction('Show in Table', MainWindow)
 
        
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/pencil29.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.actionPlotData.setIcon(icon)
        #self.actionShowCursors = QtGui.QAction(MainWindow)
        #self.actionShowCursors.setCheckable(True)
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icons/push7.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.actionShowCursors.setIcon(icon1)
        #self.actionSaveFileAs = QtGui.QAction(MainWindow)
        #self.actionZoomOut = QtGui.QAction(MainWindow)
        #icon2 = QtGui.QIcon()
        #icon2.addPixmap(QtGui.QPixmap(_fromUtf8("icons/home107.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.actionZoomOut.setIcon(icon2)
        #self.actionBaseline = QtGui.QAction(MainWindow)
        #self.actionAverage = QtGui.QAction(MainWindow)
        #self.actionStats = QtGui.QAction(MainWindow)
        #self.actionShowInTable = QtGui.QAction(MainWindow)
        #self.toolBar.addAction(self.actionNewFile)
   
        
        
        
        
        
        
        
