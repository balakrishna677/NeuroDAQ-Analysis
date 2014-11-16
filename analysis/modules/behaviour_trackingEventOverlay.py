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
        self.entryName = 'Tracking event overlay'  
        ############################################
        
        # Get main browser
        self.browser = browser          
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
          
        ############################################        


    def func(self, browser):
        """ Overlay triggered events (e.g.: visual or laser stimulation)
        over tracking trace.
        
        Plots current selected tigger data over current ploted trace
        """
    
        ############################################
        # ANALYSIS FUNCTION      
    
        # Get widgets
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget
    
        # Get selected trigger data
        item = browser.ui.workingDataTree.currentItem()
        triggers = item.data
        
        # Make sure dt is matched
        dt = plotWidget.plotDataItems[0].attrs['dt']
        item.attrs['dt'] = dt
        
        # Get trigger times (in data points)
        tarray = np.arange(0, len(triggers))
        tevents = tarray[triggers>0]

        # Make infinte vertical lines on trigger events        
        for t in tevents:
            line = pg.InfiniteLine(pos=t/dt, angle=90, movable=False, pen=pg.mkPen('k', width=2))        
            plotWidget.addItem(line)
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
        # Initialise Fitting Class
        self.dataFit = Fitting()

