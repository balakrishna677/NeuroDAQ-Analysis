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
        """ Calculate average trace from currently plotted traces.

        Options:
        1) create new entry in Working Data tree with the result
        2) plot average with orginal traces
        """
    
        ############################################
        # ANALYSIS FUNCTION
        
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget   

        # Get data 
        data = aux.get_data(browser)
    
        # Get dt 
        dt = aux.get_attr(plotWidget.plotDataItems, 'dt')[0]

        # Calculate average and make h5item for plotting
        avgData = np.mean(data,0)
        avgItem = aux.make_h5item('avg', avgData, plotWidget.plotDataItems[0].attrs)

        # Plot data
        if self.showTraces.isChecked(): 
            clear = False
        else:
            clear = True
        pgplot.browse_singleData(browser, plotWidget, avgItem, clear=clear, color='r')

        # Store data
        if self.storeResult.isChecked():
            results = []
            item = plotWidget.plotDataItems[0]
            results.append(['avg_trace', avgData, item.attrs])
            aux.save_results(browser, item.parent().text(0)+'_average', results) 
                 
        ############################################  
        
        
        
        
        
