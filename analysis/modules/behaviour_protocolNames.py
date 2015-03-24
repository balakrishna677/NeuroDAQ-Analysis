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
        self.entryName = 'Get Protocol Names'  
        ############################################
        
        # Get main browser and widgets
        self.browser = browser       
        self.plotWidget = browser.ui.dataPlotsWidget
        self.toolsWidget = browser.ui.oneDimToolStackedWidget   
        # Add entry to AnalysisSelectWidget         
        selectItem = QtGui.QStandardItem(self.entryName)
        selectWidget = self.browser.ui.behaviourToolSelect
        selectWidget.model.appendRow(selectItem)        
        # Add entry to tool selector        
        browser.customToolSelector.add_tool(self.entryName, self.func)
        # Add option widgets
        self.make_option_widgets()

    
    def make_option_widgets(self):         
        stackWidget = self.browser.ui.behaviourToolStackedWidget
        self.toolGroupBox = QtGui.QGroupBox('Options')
        self.toolOptions = []
        
        ############################################
        # WIDGETS FOR USER DEFINED OPTIONS
        #self.pixelConversion = QtGui.QLineEdit()
        #self.toolOptions.append([QtGui.QLabel('cm/pixel'), self.pixelConversion])

        ############################################        

        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Process stimulation protocol names from visual and pulse stimulation.

        Creates new tree items for each protocol and the corresponding start indices
        """

        ############################################
        # ANALYSIS FUNCTION      
    
        # Get selected item with protocol names
        item = browser.ui.workingDataTree.selectedItems()[0]

        # Get protocol names in the file
        names = []
        for n in range(len(item.data)):
            if len(item.data[n])>0: names.append(item.data[n])
        if len(names)==0:
            aux.error_box('No protocol names found')
            return
           
        # Replot data
        print names
        ############################################  





