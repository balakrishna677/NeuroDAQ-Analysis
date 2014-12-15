from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import numpy as np
from analysis import auxfuncs as aux
from util import pgplot
from widgets import *
import pyqtgraph as pg
from analysis.acq4 import filterfuncs as acq4filter
import matplotlib.gridspec as gridspec
####################################

class AnalysisModule():    

    def __init__(self, browser):    
    
        ############################################
        # NAME THAT IS LISTED IN THE TAB
        self.entryName = 'Histogram'  
        ############################################
        
        # Get main browser and widgets
        self.browser = browser       
        self.plotWidget = browser.ui.dataPlotsWidget
        self.canvas =  browser.ui.mplWidget.canvas
        self.ax = browser.ui.mplWidget.canvas.ax

        # Add entry to AnalysisSelectWidget         
        selectItem = QtGui.QStandardItem(self.entryName)
        selectWidget = self.browser.ui.graphToolSelect
        selectWidget.model.appendRow(selectItem)        
        # Add entry to tool selector        
        browser.customToolSelector.add_tool(self.entryName, self.func)
        # Add option widgets
        self.make_option_widgets()
    
    def make_option_widgets(self):         
        stackWidget = self.browser.ui.graphToolStackedWidget
        self.toolGroupBox = QtGui.QGroupBox('Options')
        self.toolOptions = []
        
        ############################################
        # WIDGETS FOR USER DEFINED OPTIONS
        self.clearAxis = QtGui.QCheckBox('Clear axis')
        self.toolOptions.append([self.clearAxis]) 
        self.binSize = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Bin size'), self.binSize])
        self.orientation = QtGui.QComboBox()
        self.orientation.addItem('vertical')
        self.orientation.addItem('horizontal')      
        self.toolOptions.append([QtGui.QLabel('Orientation'), self.orientation])
        self.type = QtGui.QComboBox()
        self.type.addItem('bar')
        self.type.addItem('barstacked')      
        self.type.addItem('step')
        self.type.addItem('stepfilled')    
        self.toolOptions.append([QtGui.QLabel('Type'), self.type])                             
        ############################################        

        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Plot histogram from selected data

        Options:
        1) clear axes
        2) bin size
        3) normalised
        4) orientation
        5) type
        6) color
        """

        ############################################
        # ANALYSIS FUNCTION      

        # Read options
        clearAxis = self.clearAxis.isChecked()
        binSize = float(self.binSize.text())
        orientation = str(self.orientation.currentText())
        histtype = str(self.type.currentText())

        # Get selected item in data tree
        traces = self.plotWidget.plotDataItems
        dt = traces[0].attrs['dt']

        # Get X and Y data and check cursors
        data, c1 = aux.get_dataRange(self.plotWidget, traces[0])             

        # Calculate number of bins
        dataRange = np.abs(data.max()-data.min())
        nbins = np.ceil(dataRange/binSize)

        # Remove all existing axes
        if clearAxis:
            for ax in self.canvas.fig.axes:
                self.canvas.fig.delaxes(ax)
       
        # Create grid
        nPlots, width_ratios = 1, [1]
        gs = gridspec.GridSpec(1, nPlots, width_ratios=width_ratios)    

        # Create subplots
        ax = []
        for plot in range(nPlots):
            ax.append(self.canvas.fig.add_subplot(gs[plot]))

        # Plot histogram
        h = ax[0].hist(data, bins=nbins, orientation=orientation, histtype=histtype,
                             normed=True, color='k')

        self.canvas.draw()
        ############################################  
#delaxes(subplot)



