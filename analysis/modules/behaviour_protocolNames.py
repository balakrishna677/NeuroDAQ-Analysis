from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import numpy as np
from analysis import auxfuncs as aux
from util import pgplot
import pyqtgraph as pg
import re
from widgets import h5Item
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
        """ Process stimulation protocols from visual and pulse stimulation.

        Creates new tree items for each protocol and the corresponding frame number,
        plus a tree item for non-triggers

        Use by selecing the item holding children with Protocol Names and Indices
        """


        ############################################
        # ANALYSIS FUNCTION      
    
        # Get names and indices from selected parent item
        names, triggers = [], []
        parentItem = browser.ui.workingDataTree.selectedItems()[0]
        for i in range(parentItem.childCount()):
            item = parentItem.child(i)
            if 'Names' in item.text(0):
               names = re.findall(r"'(.*?)'", item.data, re.DOTALL)
            elif 'Indices' in item.text(0):
               triggers = item.data
        if len(names)==0 or len(triggers)==0:   
            aux.error_box('Protocol details not found')
            return

        # Get trigger times (in data points)
        tarray = np.arange(0, len(triggers))
        self.tevents = tarray[triggers>0]

        # Iterate names and add entries to data tree
        protocols = list(set(names))
        inames = list(enumerate(names))
        protocolsItem = h5Item([str('protocols_data')])
        parentItem.addChild(protocolsItem)    
        for protocol in protocols:
            item = h5Item([str(protocol)])
            item_triggers = h5Item([str('triggers')])
            item_nontriggers = h5Item([str('non_triggers')])
            item.addChild(item_triggers)
            item.addChild(item_nontriggers)
            for i in inames:
                if i[1] == protocol:
                    triggerFrame = self.tevents[i[0]] 
                    child = h5Item(['frame_'+str(triggerFrame)])
                    child.data = [triggerFrame]
                    if triggers[triggerFrame]==1:
                        item_nontriggers.addChild(child)
                    elif triggers[triggerFrame]==2:
                        item_triggers.addChild(child)
            protocolsItem.addChild(item)

        ############################################  




