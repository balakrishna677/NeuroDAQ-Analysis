from PyQt4 import QtGui, QtCore

####################################
# ADD ADDITIONAL IMPORT MODULES HERE
import os
import numpy as np
from analysis import auxfuncs as aux
from util import pgplot
import pyqtgraph as pg
import re
from widgets import h5Item
from analysis.acq4 import filterfuncs as acq4filter
from moviepy.editor import *
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
        self.baseline = int(self.eventBaseline.text())
        self.duration = int(self.eventDuration.text())
    
        # Get names and indices from selected parent item
        self.names, self.triggers = [], []
        self.parentItem = browser.ui.workingDataTree.selectedItems()[0]
        for i in range(self.parentItem.childCount()):
            item = self.parentItem.child(i)
            if 'Names' in item.text(0):
               self.names = re.findall(r"'(.*?)'", item.data, re.DOTALL)
            elif 'Indices' in item.text(0):
               self.triggers = item.data
        if len(self.names)==0 or len(self.triggers)==0:   
            aux.warning_box('Protocol details not found',
                            infoText='Using trigger levels only')
            self.noProtocolNames()
        else:
            self.withProtocolNames()

        ############################################  
    def withProtocolNames(self):
        # Get trigger times (in data points)
        tarray = np.arange(0, len(self.triggers))
        self.tevents = tarray[self.triggers>0]

        # Iterate names and add entries to data tree
        protocols = list(set(self.names))
        inames = list(enumerate(self.names))
        protocolsItem = h5Item([str('protocols_data')])
        self.parentItem.addChild(protocolsItem)    
        if self.eventsBox.isChecked():     
            itemPath = aux.selectItem_box(self.browser)
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
                        root = self.browser.ui.workingDataTree.invisibleRootItem()
                        dataSourceItem = aux.getItemFromPath(itemPath, root, level=0)
                        #print [triggerFrame-self.baseline,triggerFrame+self.baseline]
                        if ('video' in dataSourceItem.attrs) and (dataSourceItem.attrs['video']=='True'):
                            print 'this is a video' 
                        else:
                            child.data = dataSourceItem.data[triggerFrame-self.baseline:triggerFrame+self.duration]
                            # todo: check whether there is data
                    if self.triggers[triggerFrame]==1:
                        item_nontriggers.addChild(child)
                    elif self.triggers[triggerFrame]==2:
                        item_triggers.addChild(child)
                    elif self.triggers[triggerFrame]==3:
                        item_manualtriggers.addChild(child)   
            protocolsItem.addChild(item)    

    def noProtocolNames(self):
        # Get trigger times (in data points)
        tarray = np.arange(0, len(self.triggers))
        self.tevents = tarray[self.triggers>0]

        # Iterate names and add entries to data tree
        protocolsItem = h5Item([str('protocols_data')])
        self.parentItem.addChild(protocolsItem)    
        if self.eventsBox.isChecked():     
            itemPath = aux.selectItem_box(self.browser)
            itemPath = itemPath.split('/')
            root = self.browser.ui.workingDataTree.invisibleRootItem()
            dataSourceItem = aux.getItemFromPath(itemPath, root, level=0)
            if ('video' in dataSourceItem.attrs) and (dataSourceItem.attrs['video']=='True'):
                videoEvents = True
                clip = VideoFileClip(dataSourceItem.attrs['mrl'])
        item_triggers = h5Item([str('triggers')])
        item_nontriggers = h5Item([str('non_triggers')])
        item_manualtriggers = h5Item([str('manual')])
        protocolsItem.addChild(item_triggers)
        protocolsItem.addChild(item_nontriggers)
        protocolsItem.addChild(item_manualtriggers)
        for t in self.tevents:
             triggerFrame = t
             child = h5Item(['frame_'+str(triggerFrame)]) 
                   
             # Deal with data options
             if self.eventsBox.isChecked():     
                 if videoEvents:
                     tstart = (triggerFrame-self.baseline)/clip.fps
                     tend = (triggerFrame+self.duration)/clip.fps
                     subclip = clip.subclip(tstart, tend)
                     self.makeVideoStream(subclip, child)
                 else:
                     child.data = dataSourceItem.data[triggerFrame-self.baseline:triggerFrame+self.duration]
                     # todo: check whether there is data
             if self.triggers[triggerFrame]==1:
                 item_nontriggers.addChild(child)
             elif self.triggers[triggerFrame]==2:
                 item_triggers.addChild(child)
             elif self.triggers[triggerFrame]==3:
                 item_manualtriggers.addChild(child)   
        #protocolsItem.addChild(item)    

    def makeVideoStream(self, subclip, item):
        fpath = os.path.split(self.browser.currentSaveFile)
        fdir = fpath[0]
        folder = '.'+os.path.splitext(fpath[1])[0]
        if folder not in os.listdir(fdir):
             os.mkdir(folder) 
        savename = fdir+folder+str(item.text(0))+'.mp4'
        subclip.write_videofile(savename, fps=subclip.fps)
        item.attrs['video'] = 'True'
        item.attrs['mrl'] = savename

    def set_defaultValues(self):
        self.eventBaseline.setText('200')
        self.eventDuration.setText('200')



