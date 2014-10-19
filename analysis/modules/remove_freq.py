from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import numpy as np
from analysis import auxfuncs as aux
from util import pgplot
import pyqtgraph as pg
from analysis.acq4 import filterfuncs as acq4filter
####################################

class AnalysisModule():    

    def __init__(self, browser):    
    
        ############################################
        # NAME THAT IS LISTED IN THE TAB
        self.entryName = 'Remove Frequency'  
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
        # Set default values
        self.set_defaultValues()
    
    def make_option_widgets(self):         
        stackWidget = self.browser.ui.oneDimToolStackedWidget
        self.toolGroupBox = QtGui.QGroupBox('Options')
        self.toolOptions = []
        
        ############################################
        # WIDGETS FOR USER DEFINED OPTIONS
        self.freqRemoveFrequency = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Frequency'), self.freqRemoveFrequency])  
        self.freqRemoveHarmonics = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Harmonics'), self.freqRemoveHarmonics]) 
        self.freqRemoveSamples = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Samples'), self.freqRemoveSamples])               
        ############################################        
              
        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Remove a specific frequency from the data
    
        Options:
        1) Frequency
        2) Number of harmonics
        3) Number of FFT data samples to blank centered on the Frequency  
        
        Note: frequencies are in Hz, make sure dt is in seconds
        """
    
        ############################################
        # ANALYSIS FUNCTION
        
        # Get options
        frequency = float(self.freqRemoveFrequency.text())
        harmonics = int(self.freqRemoveHarmonics.text())
        samples = int(self.freqRemoveSamples.text())
    
        # Get widgets
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget
    
        # Get parent text of plotted items
        try:
            parentText = plotWidget.plotDataItems[0].parent().text(0) # Assumes all plotted data have the same parent
        except AttributeError:   # Parent = None
            parentText = 'Data'
    
        # Remove frequency
        results = [] 
        for item in plotWidget.plotDataItems:  
            # Copy attributes and add some new ones
            attrs = item.attrs
            attrs['frequency_removed'] = frequency
        
            # Remove
            traceFilter = acq4filter.removePeriodic(item.data, frequency, float(item.attrs['dt'])/1000, harmonics, samples)
            results.append([item.text(0), traceFilter, attrs])
        
            # Store and plot filtered trace            
            filterItem = aux.make_h5item('filter', traceFilter, item.attrs)
            pgplot.browse_singleData(browser, plotWidget, filterItem, clear=False, color='#F2EF44')

        # Store results
        aux.save_results(browser, parentText+'_filter', results)     
         
        ############################################  

    def set_defaultValues(self):
        self.freqRemoveFrequency.setText('50')
        self.freqRemoveHarmonics.setText('20')
        self.freqRemoveSamples.setText('400')
