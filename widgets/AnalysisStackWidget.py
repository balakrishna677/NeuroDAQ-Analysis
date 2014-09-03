from PyQt4 import QtGui, QtCore

class AnalysisStackWidget(QtGui.QStackedWidget):

    """ Stack widget for listing 1D Analysis tool options. 
    Allows setting a size hint.    
    AnalysisSelectWidget(width, height)
    """

    def __init__(self, width, height):
        QtGui.QStackedWidget.__init__(self)
        self._width = width
        self._height = height
        self.make_options()
        
    def sizeHint(self):
        return QtCore.QSize(self._width, self._height)

    def make_options(self):
        # Baseline  (index=0)
        self.baselineTool = QtGui.QGroupBox('Options')
        self.baselineToolOptions = []
        self.baselineToolOptions.append(QtGui.QCheckBox('Keep original data', self.baselineTool))   
        make_groupBox_layout(self.baselineToolOptions, self.baselineTool)              
        self.addWidget(self.baselineTool)
        
        # Averaging  (index=1)
        self.avgTool = QtGui.QGroupBox('Options')
        self.avgToolOptions = []
        self.avgToolOptions.append(QtGui.QCheckBox('Show traces', self.avgTool))
        self.avgToolOptions.append(QtGui.QCheckBox('Store result', self.avgTool))   
        make_groupBox_layout(self.avgToolOptions, self.avgTool)     
        self.addWidget(self.avgTool)
               
        # Measure  (index=2)
        self.measureTool = QtGui.QGroupBox('Options')
        self.measureToolOptions = []
        self.measureToolOptions.append(QtGui.QCheckBox('Store result', self.measureTool))
        self.measureToolOptions.append(QtGui.QCheckBox('Minimum', self.measureTool))
        self.measureToolOptions.append(QtGui.QCheckBox('Maximum', self.measureTool))
        make_groupBox_layout(self.measureToolOptions, self.measureTool)
        self.addWidget(self.measureTool)
        
        # Event Detection  (index=3)
        self.eventTool = QtGui.QGroupBox('Options')
        self.eventToolOptions = []
        self.eventThreshold = QtGui.QLineEdit()
        self.eventToolOptions.append([QtGui.QLabel('Threshold'), self.eventThreshold])        
        self.eventNoiseSafety = QtGui.QLineEdit()
        self.eventToolOptions.append([QtGui.QLabel('Noise Safety'), self.eventNoiseSafety])
        make_label_layout(self.eventToolOptions, self.eventTool)
        self.addWidget(self.eventTool)        
        

def make_groupBox_layout(optionsList, groupBox):
    """ Layout widgets vertically
    """
    vbox = QtGui.QVBoxLayout()
    for widget in optionsList:
        vbox.addWidget(widget)
    vbox.addStretch(1)
    groupBox.setLayout(vbox)

def make_label_layout(optionsList, groupBox):
    """ Layout labels and widgets side by side, vertically
    using a grid layout 
    """
    gridbox = QtGui.QGridLayout()
    row = 0
    for item in optionsList:
        gridbox.addWidget(item[0], row, 0)
        gridbox.addWidget(item[1], row, 1)
        row+=1
    gridbox.setRowMinimumHeight(row,0)
    gridbox.setRowStretch(row,1)    
    groupBox.setLayout(gridbox)


