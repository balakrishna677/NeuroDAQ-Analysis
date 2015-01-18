from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import numpy as np
from analysis import auxfuncs as aux
from util import pgplot
import pyqtgraph as pg
####################################

class AnalysisModule():    

    def __init__(self, browser):    
    
        ############################################
        # NAME THAT IS LISTED IN THE TAB
        self.entryName = 'Trace operations'  
        ############################################
        
        # Get main browser
        self.browser = browser          
        # Add entry to AnalysisSelectWidget         
        selectItem = QtGui.QStandardItem(self.entryName)
        selectWidget = self.browser.ui.oneDimToolSelect
        selectWidget.model.appendRow(selectItem)        
        # Add entry to tool selector        
        browser.customToolSelector.add_tool(self.entryName, self.func)
        # Add option widgets
        self.make_option_widgets()

        selectItem.setToolTip('Perform operations in selected traces')
    
    def make_option_widgets(self):         
        stackWidget = self.browser.ui.oneDimToolStackedWidget
        self.toolGroupBox = QtGui.QGroupBox('Options')
        self.toolOptions = []
        
        ############################################
        # WIDGETS FOR USER DEFINED OPTIONS   
        self.keepData = QtGui.QCheckBox('Keep original data')
        self.toolOptions.append([self.keepData])
        self.delPointsBox = QtGui.QCheckBox('Delete points')
        self.toolOptions.append([self.delPointsBox])
        self.offsetBox = QtGui.QCheckBox('Offset points')
        self.offsetPoints = QtGui.QLineEdit()
        self.toolOptions.append([self.offsetBox, self.offsetPoints])
        self.scaleBox = QtGui.QCheckBox('Scale')
        self.scaleValue = QtGui.QLineEdit()
        self.toolOptions.append([self.scaleBox, self.scaleValue])

        ############################################        
              
        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Perform some operations on selected traces. 
    
        Options:
        1) keep original traces intact and create processed copies
        2) delete the data points between the cursors
        3) offset the start of the trace by a number of X-axis points (adds NaNs)
        """
    
        ############################################
        # ANALYSIS FUNCTION
        
        # Get widgets
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget

        # Get options
        if self.offsetBox.isChecked():
          try:    
            nOffsetPoints = float(self.offsetPoints.text())
          except ValueError:
            aux.error_box('Invalid number of points')
            return

        if self.scaleBox.isChecked():
          try:    
            vScale = float(self.scaleValue.text())
          except ValueError:
            aux.error_box('Invalid scale entry')
            return

        # Copy data if required
        if self.keepData.isChecked():
            aux.make_data_copy(browser, plotWidget)

        # Iterate through traces
        for item in plotWidget.plotDataItems:
            
            # Get dt and data range
            dt = item.attrs['dt']
            dataRange, c1, cx1, cx2 = aux.get_dataRange(plotWidget, item, cursors=True)
            
            # Scale data
            if self.scaleBox.isChecked():
                item.data = item.data * vScale

            # Delete points
            if self.delPointsBox.isChecked():
                item.data = np.delete(item.data, np.s_[c1:c1+len(dataRange)+1])

            # Add offset
            if self.offsetBox.isChecked():
                offset = int(nOffsetPoints/dt)
                item.data = np.insert(item.data, 0, np.zeros(offset) + np.nan)          

        # Re-plot data
        pgplot.replot(browser, plotWidget) 
          
        ############################################  

