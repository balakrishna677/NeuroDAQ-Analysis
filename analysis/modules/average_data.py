from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import numpy as np
import sys
from analysis import auxfuncs as aux
from util import pgplot
import pyqtgraph as pg
####################################

class AnalysisModule():    

    def __init__(self, browser):    
    
        ############################################
        # NAME THAT IS LISTED IN THE TAB
        self.entryName = 'Average'  
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
        self.showTraces = QtGui.QCheckBox('Show traces')
        self.storeResult = QtGui.QCheckBox('Store result')
        self.toolOptions.append(self.showTraces)
        self.toolOptions.append(self.storeResult)      
        ############################################        
              
        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Calculate average trace from currently plotted traces. If cursors are
        selected the average is calculated for the range within the cursors.

        Options:
        1) create new entry in Working Data tree with the result
        2) plot average with orginal traces
        """
    
        ############################################
        # ANALYSIS FUNCTION
        
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget   

        # Get data and cursors
        data = aux.get_data(browser)
        dataRange, c1 = aux.get_dataRange(plotWidget, plotWidget.plotDataItems[0])
        c2 = c1 + len(dataRange)    

        # Get dt 
        item = plotWidget.plotDataItems[0]
        dt = item.attrs['dt']

        # Calculate average and make h5item for plotting
        try:
            avgData = np.mean(data[:, c1:c2], 0)
            avgItem = aux.make_h5item('avg', avgData, plotWidget.plotDataItems[0].attrs)
        except ValueError:  
            aux.error_box('Cannot calculate average on data with different lengths', sys.exc_info(),
                          'Please ensure that all traces have the same length') 
            return

        # Plot data
        if self.showTraces.isChecked(): 
            clear = False
        else:
            clear = True
        pgplot.browse_singleData(browser, plotWidget, avgItem, clear=clear, color='r')

        # Store data
        if self.storeResult.isChecked():
            results = []
            results.append(['avg_trace', avgData, item.attrs])
            aux.save_results(browser, item.parent().text(0)+'_average', results) 
                 
        ############################################  
        
        
        
        
        
