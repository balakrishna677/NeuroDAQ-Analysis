from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import numpy as np
from analysis import auxfuncs as aux
from util import pgplot
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
        self.nbins = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Number of bins'), self.nbins])
        ############################################        

        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Plot histogram from selected data

        Options:
        1) number of bins
        """

        ############################################
        # ANALYSIS FUNCTION      

        # Read options
        nbins = int(self.nbins.text())

        # Get selected item in data tree
        traces = self.plotWidget.plotDataItems
        dt = traces[0].attrs['dt']

        # Get X and Y data and check cursors
        X, c1 = aux.get_dataRange(self.plotWidget, traces[0])
        Y, c1 = aux.get_dataRange(self.plotWidget, traces[1])        
       
        # Make sure Y is the long axis
        if X.max() > Y.max():
            Yold = Y
            Y = X
            X = Yold

        # Remove all existing axes
        for ax in self.canvas.fig.axes:
            self.canvas.fig.delaxes(ax)
       
        # Create grid
        if hist: 
            if axisTime:
                nPlots, width_ratios = 3, [1,4,1] 
                histAx = 2
            else:
                nPlots, width_ratios = 2, [1,1]
                histAx = 1
        elif axisTime:
            nPlots, width_ratios = 2, [1,5]
        else:
            nPlots, width_ratios = 1, [1]
        gs = gridspec.GridSpec(1, nPlots, width_ratios=width_ratios)    

        # Create subplots
        ax = []
        for plot in range(nPlots):
            ax.append(self.canvas.fig.add_subplot(gs[plot]))

        # Plot tracking
        ax[0].plot(X, Y, color)

        # Plot long axis over time
        if axisTime:
            xaxis = np.arange(0, len(Y), dt)
            ax[1].plot(xaxis, Y, color)

        # Plot histogram
        if hist:
            h = ax[histAx].hist(Y, bins=30, orientation='horizontal', histtype='stepfilled',
                               normed=True, color=color)


        self.canvas.draw()
        ############################################  
#delaxes(subplot)


