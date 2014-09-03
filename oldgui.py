# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
    
        #sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
    
        # -----------------------------------------------------------------------------
        # Central Widget
        # -----------------------------------------------------------------------------

        # Geometry and Layout
        MainWindow.resize(1300, 780)                
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(MainWindow)   
        self.gridLayout_centralwidget = QtGui.QGridLayout(self.centralwidget)
        self.splitter_centralwidget = QtGui.QSplitter(self.centralwidget)
        self.splitter_centralwidget.setOrientation(QtCore.Qt.Horizontal)


        # -----------------------------------------------------------------------------
        # Left pane -> SelectionTabs Widget and SinglePlot Widget
        # -----------------------------------------------------------------------------
        # Geometry and Layout
        self.splitter_leftPane = QtGui.QSplitter(self.splitter_centralwidget)
        self.splitter_leftPane.setOrientation(QtCore.Qt.Vertical)


        # SelectionTabs Widget
        # -----------------------------------------------------------------------------
        # Geometry and Layout             
        self.selectionTabWidget = QtGui.QTabWidget(self.splitter_leftPane)
        self.selectionTabWidget.setSizePolicy(sizePolicy)
        self.selectionTabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.selectionTabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.selectionTabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.myPolicy = self.selectionTabWidget.sizePolicy()
        self.myPolicy.setVerticalStretch(5)
        self.selectionTabWidget.setSizePolicy(self.myPolicy)        

        
        # ------
        # TAB 1   (DataTab) -> dirTree and fileDataTree
        # ------
        # Geometry and Layout
        self.dataTab = QtGui.QWidget()
        self.selectionTabWidget.addTab(self.dataTab, _fromUtf8(""))
        self.gridLayout_dataTab = QtGui.QGridLayout(self.dataTab)
        self.splitter_dataTab = QtGui.QSplitter(self.dataTab)
        self.splitter_dataTab.setSizePolicy(sizePolicy)
        self.splitter_dataTab.setOrientation(QtCore.Qt.Horizontal)
        self.gridLayout_dataTab.addWidget(self.splitter_dataTab, 0, 0, 1, 1)
               
        # TAB 1 content > DirTree
        self.dirTree = QtGui.QTreeView(self.splitter_dataTab)
        self.dirTree.setSizePolicy(sizePolicy)
        
        # TAB 1 content > FileDataTree
        self.fileDataTree = h5TreeWidget(self.splitter_dataTab)
        self.fileDataTree.setSizePolicy(sizePolicy)
        self.fileDataTree.setAcceptDrops(True)
        self.fileDataTree.setDragEnabled(True)
        self.fileDataTree.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.fileDataTree.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.fileDataTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.fileDataTree.headerItem().setText(0, _fromUtf8("1"))


        # -----
        # TAB 2   (oneDimAnalysisTab) -> toolSelect and toolStackedWidget
        # -----
        # Geometry and Layout
        self.oneDimAnalysisTab = QtGui.QWidget()
        self.selectionTabWidget.addTab(self.oneDimAnalysisTab, _fromUtf8(""))
        self.gridLayout_oneDimAnalysisTab = QtGui.QGridLayout(self.oneDimAnalysisTab)
        self.splitter_oneDimAnalysisTab = QtGui.QSplitter(self.oneDimAnalysisTab)
        self.splitter_oneDimAnalysisTab.setSizePolicy(sizePolicy)        
        self.splitter_oneDimAnalysisTab.setOrientation(QtCore.Qt.Horizontal)
        self.gridLayout_oneDimAnalysisTab.addWidget(self.splitter_oneDimAnalysisTab, 0, 0, 1, 1)

        # TAB 2 content > Tool Select        
        self.oneDimToolSelect = QtGui.QListView(self.splitter_oneDimAnalysisTab)
        self.oneDimToolSelect.setSizePolicy(sizePolicy)

        # TAB 2 content > Tools Stacked Widget        
        self.toolStackedWidget = QtGui.QStackedWidget(self.splitter_oneDimAnalysisTab)
        self.toolStackedWidget.setSizePolicy(sizePolicy)
        
        # TOOLS in Stacked Widget
        # Averaging
        self.avgTool = QtGui.QWidget()
        self.checkBox = QtGui.QCheckBox(self.avgTool)
        self.checkBox.setGeometry(QtCore.QRect(10, 30, 97, 22))
        self.toolStackedWidget.addWidget(self.avgTool)
        self.avgTool.setSizePolicy(sizePolicy)
        
        # Baseline  
        self.baselineTool = QtGui.QWidget()
        self.toolStackedWidget.addWidget(self.baselineTool)
        
        # Measure
        self.measureTool = QtGui.QWidget()
        self.toolStackedWidget.addWidget(self.measureTool)

        
        
        # SinglePlots Widget
        # -----------------------------------------------------------------------------       
        #Geometry and Layout 
        self.singlePlotWidget = matplotlibWidget(self.splitter_leftPane)
        self.singlePlotWidget.setSizePolicy(sizePolicy)
        

        # -----------------------------------------------------------------------------
        # Middle pane -> DisplayTabs Widget 
        # -----------------------------------------------------------------------------        
          
        # DisplayTabs Widget
        # -----------------------------------------------------------------------------
        # Geometry and Layout
        self.displayTabWidget = QtGui.QTabWidget(self.splitter_centralwidget)
        self.displayTabWidget.setMinimumSize(QtCore.QSize(0, 0))

        # ------
        # TAB 1   (PlotTab)
        # ------    
        # Geometry and Layout
        self.plotTab = QtGui.QWidget()
        self.gridLayout_plotTab = QtGui.QGridLayout(self.plotTab)
 
        # TAB 1 content > dataPlotsWidget
        self.dataPlotsWidget = matplotlibWidget(self.plotTab)
        sizePolicy2 = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)            
        self.dataPlotsWidget.setSizePolicy(sizePolicy)
        self.dataPlotsWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.gridLayout_plotTab.addWidget(self.dataPlotsWidget, 0, 0, 1, 1)
        self.displayTabWidget.addTab(self.plotTab, _fromUtf8(""))
        
        # ------
        # TAB 2   (TableTab)
        # ------        
        # Geometry and Layout   
        # TAB 2 content > tableWidget         
        self.tableTab = QtGui.QWidget()
        self.gridLayout_tableTab = QtGui.QGridLayout(self.tableTab)
        self.dataTableWidget = QtGui.QTableWidget(self.tableTab)
        self.dataTableWidget.setDragEnabled(True)
        self.dataTableWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.dataTableWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.dataTableWidget.setAlternatingRowColors(True)
        self.dataTableWidget.setColumnCount(0)
        self.dataTableWidget.setRowCount(0)
        self.gridLayout_tableTab.addWidget(self.dataTableWidget, 0, 0, 1, 1)
        self.displayTabWidget.addTab(self.tableTab, _fromUtf8(""))


        # -----------------------------------------------------------------------------
        # Right pane -> Working Data Tree and Properties Table
        # -----------------------------------------------------------------------------
        # Geometry and Layout      
        self.splitter_rightPane = QtGui.QSplitter(self.splitter_centralwidget)
        self.splitter_rightPane.setSizePolicy(sizePolicy)
        self.splitter_rightPane.setOrientation(QtCore.Qt.Vertical)
        
        # WorkingDataTree Widget
        # -----------------------------------------------------------------------------        
        self.workingDataTree = h5TreeWidget(self.splitter_rightPane)
        self.workingDataTree.setSizePolicy(sizePolicy)
        self.workingDataTree.setMinimumSize(QtCore.QSize(0, 0))
        self.workingDataTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workingDataTree.setAcceptDrops(True)
        self.workingDataTree.setDragEnabled(True)
        self.workingDataTree.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.workingDataTree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.workingDataTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.workingDataTree.headerItem().setText(0, _fromUtf8("1"))
        
        # Properties Table Widget
        # -----------------------------------------------------------------------------
        self.propsTableWidget = QtGui.QTableWidget(self.splitter_rightPane)
        self.propsTableWidget.setSizePolicy(sizePolicy)
        self.propsTableWidget.setRowCount(0)
        self.propsTableWidget.setColumnCount(0)
        self.propsTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.propsTableWidget.horizontalHeader().setStretchLastSection(True)

        # central widget stuff - move up?
        self.gridLayout_centralwidget.addWidget(self.splitter_centralwidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        

        # -----------------------------------------------------------------------------
        # Status Bar
        # -----------------------------------------------------------------------------        
        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        
        # -----------------------------------------------------------------------------
        # Tool Bar
        # -----------------------------------------------------------------------------
        # Geometry and Layout
        self.toolBar = QtGui.QToolBar(MainWindow)
        sizePolicy3 = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        self.toolBar.setSizePolicy(sizePolicy3)
        self.toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
                
        # Actions - some should go in mainWindow.py if they are not tied to a graphical ? 
        self.actionLoadData = QtGui.QAction(MainWindow)
        self.actionNewFile = QtGui.QAction(MainWindow)
        self.actionSaveFile = QtGui.QAction(MainWindow)
        self.actionAddRootGroup = QtGui.QAction(MainWindow)
        self.actionAddChildGroup = QtGui.QAction(MainWindow)
        self.actionAddDataset = QtGui.QAction(MainWindow)
        self.actionRenameTreeItem = QtGui.QAction(MainWindow)
        self.actionRemoveTreeItem = QtGui.QAction(MainWindow)
        self.actionPlotData = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/pencil29.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlotData.setIcon(icon)
        self.actionShowCursors = QtGui.QAction(MainWindow)
        self.actionShowCursors.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icons/push7.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShowCursors.setIcon(icon1)
        self.actionSaveFileAs = QtGui.QAction(MainWindow)
        self.actionZoomOut = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("icons/home107.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon2)
        self.actionBaseline = QtGui.QAction(MainWindow)
        self.actionAverage = QtGui.QAction(MainWindow)
        self.actionStats = QtGui.QAction(MainWindow)
        self.actionShowInTable = QtGui.QAction(MainWindow)
        self.toolBar.addAction(self.actionNewFile)
        self.toolBar.addAction(self.actionLoadData)
        self.toolBar.addAction(self.actionSaveFile)
        self.toolBar.addAction(self.actionSaveFileAs)

        self.retranslateUi(MainWindow)
        self.selectionTabWidget.setCurrentIndex(1)
        self.toolStackedWidget.setCurrentIndex(0)
        self.displayTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "NeuroDAQ Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.selectionTabWidget.setTabText(self.selectionTabWidget.indexOf(self.dataTab), QtGui.QApplication.translate("MainWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.selectionTabWidget.setTabText(self.selectionTabWidget.indexOf(self.oneDimAnalysisTab), QtGui.QApplication.translate("MainWindow", "1D Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.displayTabWidget.setTabText(self.displayTabWidget.indexOf(self.plotTab), QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.displayTabWidget.setTabText(self.displayTabWidget.indexOf(self.tableTab), QtGui.QApplication.translate("MainWindow", "Table", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoadData.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoadData.setToolTip(QtGui.QApplication.translate("MainWindow", "Load data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFile.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFile.setToolTip(QtGui.QApplication.translate("MainWindow", "New File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveFile.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddRootGroup.setText(QtGui.QApplication.translate("MainWindow", "Add Root Group", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddChildGroup.setText(QtGui.QApplication.translate("MainWindow", "Add Child Group", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddDataset.setText(QtGui.QApplication.translate("MainWindow", "Add Dataset", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRenameTreeItem.setText(QtGui.QApplication.translate("MainWindow", "Rename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemoveTreeItem.setText(QtGui.QApplication.translate("MainWindow", "Remove Item", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotData.setText(QtGui.QApplication.translate("MainWindow", "plotData", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotData.setToolTip(QtGui.QApplication.translate("MainWindow", "Plot Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowCursors.setText(QtGui.QApplication.translate("MainWindow", "showCursors", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowCursors.setToolTip(QtGui.QApplication.translate("MainWindow", "Show Cursors", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveFileAs.setText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomOut.setToolTip(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBaseline.setText(QtGui.QApplication.translate("MainWindow", "Baseline", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBaseline.setToolTip(QtGui.QApplication.translate("MainWindow", "Baseline traces", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAverage.setText(QtGui.QApplication.translate("MainWindow", "Average", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAverage.setToolTip(QtGui.QApplication.translate("MainWindow", "Make Average", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStats.setText(QtGui.QApplication.translate("MainWindow", "Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStats.setToolTip(QtGui.QApplication.translate("MainWindow", "Measure Statistics", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowInTable.setText(QtGui.QApplication.translate("MainWindow", "Show in Table", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidgetFile import matplotlibWidget
from h5TreeWidgetFile import h5TreeWidget
