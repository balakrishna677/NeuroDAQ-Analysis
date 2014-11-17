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
        self.entryName = 'Event extract'  
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
        self.eventBaseline = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Baseline'), self.eventBaseline])
        self.eventDuration = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Duration'), self.eventDuration])             
        ############################################        

        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Extract snippets of tracking trace triggered on events trace
        (e.g.: loom or laser stimulation)

        Analyses the currently plotted tracking trace with the currently
        selected event trigger trace
        """
    
        ############################################
        # ANALYSIS FUNCTION      

        # Read options 
        baseline = float(self.eventBaseline.text())
        duration = float(self.eventDuration.text())
   
        # Get widgets
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget
    
        # Get plotted tracking data
        trackData = plotWidget.plotDataItems[0].data

        # Get selected trigger data
        item = browser.ui.workingDataTree.currentItem()
        triggers = item.data
        
        # Make sure dt is matched
        dt = plotWidget.plotDataItems[0].attrs['dt']
        item.attrs['dt'] = dt
        
        # Get trigger times (in data points)
        tarray = np.arange(0, len(triggers))
        tevents = tarray[triggers>0]

        # Extract events        
        events = []
        for t in tevents:
            event = trackData[t-int(baseline/dt):t+int(duration/dt)]
            events.append(event)

        # Store data
        results = []
        attrs = {}
        attrs['dt'] = dt 
        for e in np.arange(0, len(events)):
            results.append(['event'+str(e), events[e], attrs])  
        aux.save_results(self.browser, 'Events', results)        
        ############################################  
       





