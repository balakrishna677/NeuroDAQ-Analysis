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
        self.entryName = 'Measure'  
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

    
    def make_option_widgets(self):         
        stackWidget = self.browser.ui.oneDimToolStackedWidget
        self.toolGroupBox = QtGui.QGroupBox('Options')
        self.toolOptions = []
        
        ############################################
        # WIDGETS FOR USER DEFINED OPTIONS   
        self.storeBox = QtGui.QCheckBox('Store results')
        self.toolOptions.append([self.storeBox])
        self.minBox = QtGui.QCheckBox('Minimum')
        self.toolOptions.append([self.minBox])
        self.maxBox = QtGui.QCheckBox('Maximum')
        self.toolOptions.append([self.maxBox])
        self.meanBox = QtGui.QCheckBox('Mean')
        self.toolOptions.append([self.meanBox])
        ############################################        
              
        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Measure selected properties or statistics in the region defined
        by the data cursors.
    
        Options:
        1) create new entries in Working Data tree with the results
        """
    
        ############################################
        # ANALYSIS FUNCTION
        
        # Get widgets
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget

        # Iterate through traces
        dataMin, dataMax, dataMean = [], [], []
        for item in plotWidget.plotDataItems:
            
            # Get dt and data range
            dt = item.attrs['dt']
            data, c1, cx1, cx2 = aux.get_dataRange(plotWidget, item, cursors=True)
            
            # Measure selected parameters
            if self.minBox.isChecked():
                y = np.min(data)
                x = np.argmin(data)
                dataMin.append(y)
                aux.plot_point(plotWidget, c1, x, y, dt)                

            if self.maxBox.isChecked():
                y = np.max(data)
                x = np.argmax(data)
                dataMax.append(y)
                aux.plot_point(plotWidget, c1, x, y, dt)  

            if self.meanBox.isChecked():
                y = np.mean(data)
                dataMean.append(y)
                plotWidget.plot([cx1,cx2], [y,y], pen=pg.mkPen('#CF1C04', width=1))  

        # Store results
        results = []
        if self.storeBox.isChecked():
            if self.minBox.isChecked(): results.append(['Minimum', dataMin])
            if self.maxBox.isChecked(): results.append(['Maximum', dataMax])
            if self.meanBox.isChecked(): results.append(['Mean', dataMean])
            aux.save_results(browser, 'Measurements', results)             
        ############################################  

