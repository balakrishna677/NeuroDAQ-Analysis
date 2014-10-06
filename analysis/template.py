""" Template for adding new analysis modules.
"""

from PyQt4 import QtGui, QtCore

class AnalysisModule():    

    def __init__(self, browser):        
        entryName = 'myModule'  
        self.browser = browser  
        # Add entry to AnalysisSelectWidget         
        selectItem = QtGui.QStandardItem(entryName)
        selectWidget = self.browser.ui.customToolSelect
        selectWidget.model.appendRow(selectItem)
        
        # Add entry to tool selector        
        browser.customToolSelector.add_tool(entryName, self.func)

        # Add option widgets
        self.make_option_widgets()

    def make_option_widgets(self):          
        stackWidget = self.browser.ui.customToolStackedWidget
        self.toolGroupBox = QtGui.QGroupBox('Options')
        self.toolOptions = []
        
        # Options go here
        self.toolOptions.append(QtGui.QCheckBox('myOption 1', self.toolGroupBox))
        
        stackWidget.add_options(self.toolOptions, self.toolGroupBox)


    def func(self, browser):
        print 'My custom analysis function'
