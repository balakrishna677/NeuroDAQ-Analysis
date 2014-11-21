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
        self.entryName = 'Get trigger Events'  
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
        self.trigger = QtGui.QComboBox()
        self.trigger.addItem('1')
        self.trigger.addItem('2')
        self.trigger.addItem('3')
        self.triggerLabel = QtGui.QLabel('Trigger level')
        self.toolOptions.append([self.triggerLabel, self.trigger])
        self.eventBaseline = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Baseline'), self.eventBaseline])
        self.eventDuration = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Duration'), self.eventDuration]) 
        #self.eventCutOut = QtGui.QPushButton('Cut events')
        #self.toolOptions.append([self.eventCutOut])          

        # Connect buttons to functions
        #self.eventCutOut.clicked.connect(self.event_cut) 
        ############################################        

        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Analyse tracking data using triggered events 
        (e.g.: visual or laser stimulation)
  
        Analyses the currently plotted tracking trace with the currently
        selected event trigger trace.

        Main function overlays triggered events on tracking trace and gets
        trigger times for event cut out.

        Event Cut: extract snippets of tracking trace triggered on events trace
        (e.g.: loom or laser stimulation)

        Options:
        1) Baseline and Duration for event cut out
        """

        ############################################
        # ANALYSIS FUNCTION      
    
        # Read options
        level = int(self.trigger.currentText())

        # Get widgets
        self.plotWidget = browser.ui.dataPlotsWidget
        self.toolsWidget = browser.ui.oneDimToolStackedWidget
    
        # Get selected trigger data
        item = self.browser.ui.workingDataTree.currentItem()
        triggers = item.data
        
        # Make sure dt is matched
        dt = self.plotWidget.plotDataItems[0].attrs['dt']
        item.attrs['dt'] = dt
        
        # Get trigger times (in data points)
        tarray = np.arange(0, len(triggers))
        self.tevents = tarray[triggers==level]

        # Make infinte vertical lines on trigger events        
        for t in self.tevents:
            line = pg.InfiniteLine(pos=t*dt, angle=90, movable=False, pen=pg.mkPen('k', width=2))        
            self.plotWidget.addItem(line)

        # Automatically cut events
        self.event_cut()
        ############################################  

    def event_cut(self):

        # Read options 
        baseline = float(self.eventBaseline.text())
        duration = float(self.eventDuration.text())
    
        # Get plotted tracking data
        trackData = self.plotWidget.plotDataItems[0].data

        # Get selected trigger data
        item = self.browser.ui.workingDataTree.currentItem()
        triggers = item.data
        
        # Deal with dt
        dt = self.plotWidget.plotDataItems[0].attrs['dt']
        item.attrs['dt'] = dt

        # Extract events        
        events = []
        for t in self.tevents:
            event = trackData[t-int(baseline/dt):t+int(duration/dt)]
            events.append(event)

        # Store data
        results = []
        attrs = {}
        attrs['dt'] = dt 
        attrs['t0'] = baseline  # in sampling points
        for e in np.arange(0, len(events)):
            attrs['trigger_time'] = self.tevents[e]  # in sampling points 
            results.append(['event'+str(e), events[e], attrs])  
        aux.save_results(self.browser, 'Events', results)        
        ############################################  
       





