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
        self.entryName = 'Get Protocol Data'  
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
        # Set default values
        self.set_defaultValues() 
    
    def make_option_widgets(self):         
        stackWidget = self.browser.ui.behaviourToolStackedWidget
        self.toolGroupBox = QtGui.QGroupBox('Options')
        self.toolOptions = []
        
        ############################################
        # WIDGETS FOR USER DEFINED OPTIONS
        self.eventsBox = QtGui.QCheckBox('Get events')
        self.toolOptions.append([self.eventsBox])
        self.eventBaseline = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Baseline'), self.eventBaseline])
        self.eventDuration = QtGui.QLineEdit()
        self.toolOptions.append([QtGui.QLabel('Duration'), self.eventDuration]) 
        ############################################        

        stackWidget.add_options(self.toolOptions, self.toolGroupBox, self.entryName)

    def func(self, browser):
        """ Process stimulation protocols from visual and pulse stimulation.

        Creates new tree items for each protocol and the corresponding frame number,
        plus a tree item for non-triggers

        Use by selecing the item holding children with Protocol Names and Indices

        Options:
        1) get events 
        """


        ############################################
        # ANALYSIS FUNCTION      

        # Read options 
        baseline = int(self.eventBaseline.text())
        duration = int(self.eventDuration.text())
    
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
        if self.eventsBox.isChecked():     
            itemPath = aux.selectItem_box(browser)
            itemPath = itemPath.split('/')
        for protocol in protocols:
            item = h5Item([str(protocol)])
            item_triggers = h5Item([str('triggers')])
            item_nontriggers = h5Item([str('non_triggers')])
            item_manualtriggers = h5Item([str('manual')])
            item.addChild(item_triggers)
            item.addChild(item_nontriggers)
            item.addChild(item_manualtriggers)
            for i in inames:
                if i[1] == protocol:
                    triggerFrame = self.tevents[i[0]] 
                    child = h5Item(['frame_'+str(triggerFrame)])
                    
                    # Deal with data options
                    if self.eventsBox.isChecked():     
                        root = browser.ui.workingDataTree.invisibleRootItem()
                        dataSourceItem = aux.getItemFromPath(itemPath, root, level=0)
                        print [triggerFrame-baseline,triggerFrame+baseline]
                        child.data = dataSourceItem.data[triggerFrame-baseline:triggerFrame+baseline]
                        # check whether there is data

                    if triggers[triggerFrame]==1:
                        item_nontriggers.addChild(child)
                    elif triggers[triggerFrame]==2:
                        item_triggers.addChild(child)
                    elif triggers[triggerFrame]==3:
                        item_manualtriggers.addChild(child)   
            protocolsItem.addChild(item)

        ############################################  

    def event_cut(self, profile=False):

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
        events, stimProfiles = [], []
        for t in self.tevents:
            event = trackData[t-int(baseline/dt):t+int(duration/dt)]
            events.append(event)
            if profile:
                eventProfile = self.triggerProfileData[t-int(baseline/dt):t+int(duration/dt)]
                stimProfiles.append(eventProfile)                

        # Store data
        results = []
        attrs = {}
        attrs['dt'] = dt 
        attrs['t0'] = baseline  # in sampling points
        for e in np.arange(0, len(events)):
            attrs['trigger_time'] = self.tevents[e]  # in sampling points 
            results.append(['event'+str(e), events[e], attrs])  
        aux.save_results(self.browser, 'Events', results)
                
        if profile:
            results = []
            for e in np.arange(0, len(stimProfiles)):
                attrs['trigger_time'] = self.tevents[e]  # in sampling points 
                results.append(['stim'+str(e), stimProfiles[e], attrs])  
            aux.save_results(self.browser, 'Stimulation Profiles', results)     
        

    def set_defaultValues(self):
        self.eventBaseline.setText('200')
        self.eventDuration.setText('200')



