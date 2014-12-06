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
        self.entryName = 'Event probability'  
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
        self.eventDirection = QtGui.QComboBox()
        self.eventDirection.addItem('negative')
        self.eventDirection.addItem('positive')
        self.toolOptions.append([self.eventDirection])
        self.timeBin = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Time bin'), self.timeBin])
        self.apThreshold = QtGui.QPushButton('Set event threshold')
        self.apThreshold.setCheckable(True)
        self.apThresholdDisplay = QtGui.QLabel('None')
        self.toolOptions.append([self.apThreshold, self.apThresholdDisplay])   

        # Connect buttons to functions
        self.apThreshold.toggled.connect(self.show_thresholdCursor)             
        ############################################        
              
        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Calculate the probability of having an event per time bin
        Very simple threshold crossing event detection.    

        Options:
        1) Threshold for detecting spikes
        2) Time bin size
        3) Event direction
        """
    
        ############################################
        # ANALYSIS FUNCTION
        
        # Read detection options 
        threshold = float(self.browser.ui.dataPlotsWidget.cursorThsPos)
        direction = str(self.eventDirection.currentText())
        timeBin = float(self.timeBin.text())
    
        # Get widgets
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget
        plotWidget.clear()
    
        # Get parent text of plotted items
        try:
            parentText = plotWidget.plotDataItems[0].parent().text(0) # Assumes all plotted data have the same parent
        except AttributeError:   # Parent = None
            parentText = 'Data'
    
        # Detect events in each trace
        if direction=='negative':
            comp = lambda a, b: a < b
        elif direction=='positive':
            comp = lambda a, b: a > b
  
        results = []        
        for item in plotWidget.plotDataItems:
           #c1, c2 = aux.get_cursors(self.browser.ui.dataPlotsWidget)  
            dt = item.attrs['dt']

            # Check cursor range
            #c1, c2 = aux.check_cursors(c1, c2, item.data, dt)
            #data = item.data[c1/dt:c2/dt]
            data = item.data
            apCounter, i = 0, 0
            xOnsets, yOnsets  = [], []
            while i<len(data):
                if comp(data[i],threshold):
                    xOnsets.append(i)
                    yOnsets.append(data[i])
                    apCounter+=1
                    while i<len(data) and comp(data[i],threshold):
                        i+=1 # skip values if index in bounds AND until the value is below/above threshold again
                else:
                    i+=1
            
            # Get events per time bin
            binSize = int(timeBin/dt)
            nbins = np.ceil(len(data)/binSize)
            eventCounter = []
            for b in np.arange(1, nbins):
                count = np.sum((xOnsets>(b-1)*binSize) & (xOnsets<(b*binSize)))
                eventCounter.append(count)

            # Store data     
            results.append(['event_counts', eventCounter]) 

            # Plot detected events
            self.show_events(data, np.array(xOnsets), np.array(yOnsets), dt)  

        # Store results
        aux.save_results(browser, parentText+'_eventProbability', results)     
         
        ############################################  

    def show_thresholdCursor(self):
        """ Show horizontal cursor to set threshold 
        """
        plotWidget = self.browser.ui.dataPlotsWidget
        if self.apThreshold.isChecked():   
            plotWidget.cursorThsPos = 0
            plotWidget.cursorThs = pg.InfiniteLine(pos=plotWidget.cursorThsPos, angle=0, movable=True,
                                               pen=pg.mkPen('#FFD000', width=2))
            plotWidget.addItem(plotWidget.cursorThs)
            plotWidget.cursorThs.sigPositionChanged.connect(self.update_threshold)
        else:
            plotWidget.cursorThsPos = []
            plotWidget.removeItem(plotWidget.cursorThs)                    

        
    def update_threshold(self):
        plotWidget = self.browser.ui.dataPlotsWidget
        plotWidget.cursorThsPos = round(plotWidget.cursorThs.value(),2)
        self.apThresholdDisplay.setText(str(plotWidget.cursorThsPos))

    def show_events(self, data, xOnsets, yOnsets, dt):
        plotWidget = self.browser.ui.dataPlotsWidget
        x = pgplot.make_xvector(data, dt)
        plotWidget.plot(x, data)
        plotWidget.plot(xOnsets*dt, yOnsets, pen=None, symbol='o', symbolPen='r', symbolBrush=None, symbolSize=4)

#/home/tiago/Data/isilon-science/Zina/e-physHDF5/

