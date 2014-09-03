# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'browser.ui'
#
# Created: Thu Aug 21 22:56:55 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
    
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

# gridLayout_4  - gridLayout_centralwidget
# splitter_5 - splitter_centralwidget
# splitter_4 - splitter_selectionTabs_singlePlot
# gridLayout_5 - gridLayout_dataTab
# splitter - splitter_dataTab
    
        # -----------------------------------------------------------------------------
        # Central Widget
        # -----------------------------------------------------------------------------

        # Geometry
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1300, 780)                
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())         
        # Layout
        self.gridLayout_centralwidget = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_centralWidget.setObjectName(_fromUtf8("gridLayout_centralwidget"))
        self.splitter_centralwidget = QtGui.QSplitter(self.centralwidget)
        self.splitter_centralwidget.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_centralwidget.setObjectName(_fromUtf8("splitter_centralwidget"))        


        # -----------------------------------------------------------------------------
        # Left pane -> SelectionTabs Widget and SinglePlot Widget
        # -----------------------------------------------------------------------------
        # Layout
        self.splitter_selectionTabs_singlePlot = QtGui.QSplitter(self.splitter_centralwidget)
        self.splitter_selectionTabs_singlePlot.setOrientation(QtCore.Qt.Vertical)
        self.splitter_selectionTabs_singlePlot.setObjectName(_fromUtf8("splitter_selectionTabs_singlePlot"))
        self.selectionTabWidget = QtGui.QTabWidget(self.splitter_selectionTabs_singlePlot)


        # SelectionTabs Widget
        # -----------------------------------------------------------------------------
        # Geometry
        sizePolicy.setHeightForWidth(self.selectionTabWidget.sizePolicy().hasHeightForWidth())                
        self.selectionTabWidget.setSizePolicy(sizePolicy)
        self.selectionTabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.selectionTabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.selectionTabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.selectionTabWidget.setObjectName(_fromUtf8("selectionTabWidget"))
        
        # ------
        # TAB 1   (DataTab) -> dirTree and fileDataTree
        # ------
        # Layout 
        self.dataTab = QtGui.QWidget()
        self.dataTab.setObjectName(_fromUtf8("dataTab"))
        self.gridLayout_dataTab = QtGui.QGridLayout(self.dataTab)
        self.gridLayout_dataTab.setObjectName(_fromUtf8("gridLayout_dataTab"))
        self.splitter_dataTab = QtGui.QSplitter(self.dataTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter_dataTab.setSizePolicy(sizePolicy)
        self.splitter_dataTab.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_dataTab.setObjectName(_fromUtf8("splitter_dataTab"))
               
        # TAB 1 content > DirTree
        self.dirTree = QtGui.QTreeView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dirTree.sizePolicy().hasHeightForWidth())
        self.dirTree.setSizePolicy(sizePolicy)
        self.dirTree.setMinimumSize(QtCore.QSize(0, 0))
        self.dirTree.setObjectName(_fromUtf8("dirTree"))
        
        # TAB 1 content > FileDataTree
        self.fileDataTree = h5TreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileDataTree.sizePolicy().hasHeightForWidth())
        self.fileDataTree.setSizePolicy(sizePolicy)
        self.fileDataTree.setMinimumSize(QtCore.QSize(0, 0))
        self.fileDataTree.setAcceptDrops(True)
        self.fileDataTree.setDragEnabled(True)
        self.fileDataTree.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.fileDataTree.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.fileDataTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.fileDataTree.setObjectName(_fromUtf8("fileDataTree"))
        self.fileDataTree.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout_5.addWidget(self.splitter, 0, 0, 1, 1)
        self.selectionTabWidget.addTab(self.dataTab, _fromUtf8(""))

        # -----
        # TAB 2   (oneDimAnalysisTab) ->
        # -----
        self.oneDimAnalysisTab = QtGui.QWidget()
        self.oneDimAnalysisTab.setObjectName(_fromUtf8("oneDimAnalysisTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.oneDimAnalysisTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter_2 = QtGui.QSplitter(self.oneDimAnalysisTab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.oneDimToolSelect = QtGui.QListView(self.splitter_2)
        self.oneDimToolSelect.setObjectName(_fromUtf8("oneDimToolSelect"))
        self.stackedWidget = QtGui.QStackedWidget(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.avgTool = QtGui.QWidget()
        self.avgTool.setObjectName(_fromUtf8("avgTool"))
        self.checkBox = QtGui.QCheckBox(self.avgTool)
        self.checkBox.setGeometry(QtCore.QRect(10, 30, 97, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.stackedWidget.addWidget(self.avgTool)
        self.baselineTool = QtGui.QWidget()
        self.baselineTool.setObjectName(_fromUtf8("baselineTool"))
        self.stackedWidget.addWidget(self.baselineTool)
        self.measureTool = QtGui.QWidget()
        self.measureTool.setObjectName(_fromUtf8("measureTool"))
        self.stackedWidget.addWidget(self.measureTool)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout_3.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.selectionTabWidget.addTab(self.oneDimAnalysisTab, _fromUtf8(""))
        self.singlePlotWidget = matplotlibWidget(self.splitter_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singlePlotWidget.sizePolicy().hasHeightForWidth())
        self.singlePlotWidget.setSizePolicy(sizePolicy)
        self.singlePlotWidget.setObjectName(_fromUtf8("singlePlotWidget"))
        self.displayTabWidget = QtGui.QTabWidget(self.splitter_5)
        self.displayTabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.displayTabWidget.setObjectName(_fromUtf8("displayTabWidget"))
        self.plotTab = QtGui.QWidget()
        self.plotTab.setObjectName(_fromUtf8("plotTab"))
        self.gridLayout = QtGui.QGridLayout(self.plotTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dataPlotsWidget = matplotlibWidget(self.plotTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataPlotsWidget.sizePolicy().hasHeightForWidth())
        self.dataPlotsWidget.setSizePolicy(sizePolicy)
        self.dataPlotsWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.dataPlotsWidget.setObjectName(_fromUtf8("dataPlotsWidget"))
        self.gridLayout.addWidget(self.dataPlotsWidget, 0, 0, 1, 1)
        self.displayTabWidget.addTab(self.plotTab, _fromUtf8(""))
        self.tableTab = QtGui.QWidget()
        self.tableTab.setObjectName(_fromUtf8("tableTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tableTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.dataTableWidget = QtGui.QTableWidget(self.tableTab)
        self.dataTableWidget.setDragEnabled(True)
        self.dataTableWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.dataTableWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.dataTableWidget.setAlternatingRowColors(True)
        self.dataTableWidget.setObjectName(_fromUtf8("dataTableWidget"))
        self.dataTableWidget.setColumnCount(0)
        self.dataTableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.dataTableWidget, 0, 0, 1, 1)
        self.displayTabWidget.addTab(self.tableTab, _fromUtf8(""))
        self.splitter_3 = QtGui.QSplitter(self.splitter_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.workingDataTree = h5TreeWidget(self.splitter_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workingDataTree.sizePolicy().hasHeightForWidth())
        self.workingDataTree.setSizePolicy(sizePolicy)
        self.workingDataTree.setMinimumSize(QtCore.QSize(0, 0))
        self.workingDataTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.workingDataTree.setAcceptDrops(True)
        self.workingDataTree.setDragEnabled(True)
        self.workingDataTree.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.workingDataTree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.workingDataTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.workingDataTree.setObjectName(_fromUtf8("workingDataTree"))
        self.workingDataTree.headerItem().setText(0, _fromUtf8("1"))
        self.propsTableWidget = QtGui.QTableWidget(self.splitter_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propsTableWidget.sizePolicy().hasHeightForWidth())
        self.propsTableWidget.setSizePolicy(sizePolicy)
        self.propsTableWidget.setRowCount(0)
        self.propsTableWidget.setColumnCount(0)
        self.propsTableWidget.setObjectName(_fromUtf8("propsTableWidget"))
        self.propsTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.propsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_4.addWidget(self.splitter_5, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoadData = QtGui.QAction(MainWindow)
        self.actionLoadData.setObjectName(_fromUtf8("actionLoadData"))
        self.actionNewFile = QtGui.QAction(MainWindow)
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionSaveFile = QtGui.QAction(MainWindow)
        self.actionSaveFile.setObjectName(_fromUtf8("actionSaveFile"))
        self.actionAddRootGroup = QtGui.QAction(MainWindow)
        self.actionAddRootGroup.setObjectName(_fromUtf8("actionAddRootGroup"))
        self.actionAddChildGroup = QtGui.QAction(MainWindow)
        self.actionAddChildGroup.setObjectName(_fromUtf8("actionAddChildGroup"))
        self.actionAddDataset = QtGui.QAction(MainWindow)
        self.actionAddDataset.setObjectName(_fromUtf8("actionAddDataset"))
        self.actionRenameTreeItem = QtGui.QAction(MainWindow)
        self.actionRenameTreeItem.setObjectName(_fromUtf8("actionRenameTreeItem"))
        self.actionRemoveTreeItem = QtGui.QAction(MainWindow)
        self.actionRemoveTreeItem.setObjectName(_fromUtf8("actionRemoveTreeItem"))
        self.actionPlotData = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/pencil29.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlotData.setIcon(icon)
        self.actionPlotData.setObjectName(_fromUtf8("actionPlotData"))
        self.actionShowCursors = QtGui.QAction(MainWindow)
        self.actionShowCursors.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icons/push7.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShowCursors.setIcon(icon1)
        self.actionShowCursors.setObjectName(_fromUtf8("actionShowCursors"))
        self.actionSaveFileAs = QtGui.QAction(MainWindow)
        self.actionSaveFileAs.setObjectName(_fromUtf8("actionSaveFileAs"))
        self.actionZoomOut = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("icons/home107.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon2)
        self.actionZoomOut.setObjectName(_fromUtf8("actionZoomOut"))
        self.actionBaseline = QtGui.QAction(MainWindow)
        self.actionBaseline.setObjectName(_fromUtf8("actionBaseline"))
        self.actionAverage = QtGui.QAction(MainWindow)
        self.actionAverage.setObjectName(_fromUtf8("actionAverage"))
        self.actionStats = QtGui.QAction(MainWindow)
        self.actionStats.setObjectName(_fromUtf8("actionStats"))
        self.actionShowInTable = QtGui.QAction(MainWindow)
        self.actionShowInTable.setObjectName(_fromUtf8("actionShowInTable"))
        self.toolBar.addAction(self.actionNewFile)
        self.toolBar.addAction(self.actionLoadData)
        self.toolBar.addAction(self.actionSaveFile)
        self.toolBar.addAction(self.actionSaveFileAs)

        self.retranslateUi(MainWindow)
        self.selectionTabWidget.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)
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
