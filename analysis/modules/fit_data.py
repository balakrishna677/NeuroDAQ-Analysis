from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from analysis import auxfuncs as aux
from util import pgplot
import pyqtgraph as pg
from analysis import smooth
####################################

class AnalysisModule():    

    def __init__(self, browser):    
    
        ############################################
        # NAME THAT IS LISTED IN THE TAB
        self.entryName = 'Fit'  
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
        self.toolGroupBox = QtGui.QGroupBox('Function')
        self.toolOptions = []
        
        ############################################
        # WIDGETS FOR USER DEFINED OPTIONS
        self.comboBox = QtGui.QComboBox()
        self.comboBox.addItem('linear')
        self.comboBox.addItem('exp')
        self.toolOptions.append([self.comboBox])

        self.toolOptions.append([QtGui.QLabel('y = a.x + b')])
        self.toolOptions.append([QtGui.QLabel('Initial guess')])
        self.p1 = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('a'), self.p1])    
        self.p2 = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('b'), self.p2])    
        ############################################        
              
        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)


    def func(self, browser):
        """ Fit data traces within cursor-defined range
    
        Options:
        1) Equation
        2) Initial guesses
        """
    
        ############################################
        # ANALYSIS FUNCTION
        
        # Get options
        #window = str(self.comboBox.currentText())
        #window_len = float(self.smoothLength.text())
    
        # Get widgets
        plotWidget = browser.ui.dataPlotsWidget
        toolsWidget = browser.ui.oneDimToolStackedWidget
        c1, c2 = aux.get_cursors(plotWidget) 
    
        # Get parent text of plotted items
        try:
            parentText = plotWidget.plotDataItems[0].parent().text(0) # Assumes all plotted data have the same parent
        except AttributeError:   # Parent = None
            parentText = 'Data'
    
        # Initialise Fitting Class
        dataFit = Fitting()

        # Fit data
        results = [] 
        for item in plotWidget.plotDataItems:  

            # Get data range to fit
            dt = item.attrs['dt']
            yData = item.data[c1/dt:c2/dt]
            xRange = np.arange(c1, c2, dt)
        
            # Fit
            fitParams = fit(fitFunc2, xRange, yData, [0.0, -1.0, c1, 20.0]) 
            print fitParams
            #results.append([item.text(0), traceSmooth, attrs])
        
            # Plot fitted function over trace
            fittedTrace = fitFunc2(xRange, fitParams[0], fitParams[1], fitParams[2], fitParams[3])
            plotWidget.plot(xRange, fittedTrace, pen=pg.mkPen('r', width=1))
            plt.plot(xRange, yData)
            plt.plot(xRange, fittedTrace, 'r')
            plt.show()

            #x = np.arange(0, len(traceSmooth)*item.attrs['dt'], item.attrs['dt'])
            #plotWidget.plot(x, traceSmooth, pen=pg.mkPen('#F2EF44', width=1))            
            #smoothItem = aux.make_h5item('smooth', traceSmooth, item.attrs)
            #pgplot.browse_singleData(browser, plotWidget, smoothItem, clear=False, color='#F2EF44')

        # Store results
        #aux.save_results(browser, parentText+'_smooth', results)     
         
        ############################################  

def fitFunc2(x, p1, p2, p3, p4):
    y = p1 + p2 * np.exp(-(x+p3)/p4)
    return y

def fitFunc(x, p1, p2):
    y = p1 + p2*x
    return y
      
def fit(fitFunc, x, y, p0):
    fitParams, fitCovariances = curve_fit(fitFunc, x, y, p0)  
    return fitParams



class Fitting():
    """ Class for fitting data.
    Dictionary with functions contains: function call, initial parameters, names
    of parameters

    Based on Fitting.py from acq4 by Paul Manis 
    (https://github.com/acq4/acq4/blob/develop/acq4/analysis/tools/Fitting.py)
    """

    def __init__(self):
        self.fitfuncmap = {
        'exp1'  : (self.exp1, [0.0, 1.0, 20.0], ['DC', 'A0', 'tau']),
        'exp2'  : (self.exp2, [0.0, 0.0, 20.0, 0.0, 0.0, 20.0], ['DC', 'A0', 'tau0', 'A1', 'tau1']),
        'parab' : (self.parab, [-10.0, 10.0, 0.0], ['i', 'N', 'bsl']),
        }

    def exp1old(self, x, p):
        """ Exponential function with amplitude and offset
        """
        y = p[0] + p[1] * np.exp(-x/p[2])
        return y

    def exp1(self, x, p1, p2, p3):
        """ Exponential function with amplitude and offset
        """
        y = p1 + p2 * np.exp(-x/p3)
        return y

    def exp2(self, x, p):
        """ Sum of two exponentials with independent time constants and amplitudes,
        and a DC offset
        """
        y = p[0] + (p[1]*np.exp(-x/p[2])) + (p[3]*np.exp(-x/p[4]))    
        return y

    def parab(self, x, p):
        """ Parabolic function for variance-mean analysis with basline variance
        """
        y = p[0] * x - (x**2)/p[1] + p[2]
        return y

    def fit(self, fitFunc, x, y, p0):
        fitParams, fitCovariances = curve_fit(fitFunc, x, y, p0)  
        return fitParams

#/home/tiago/Data/isilon-science/Analysis/AdamAnalysisHdf5/fDep_ChR2/VGAT_NPY/ctrl-70mV


