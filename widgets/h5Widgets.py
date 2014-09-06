import h5py
import sip

from PyQt4 import QtGui, QtCore


class h5Item(QtGui.QTreeWidgetItem):

    """ HDF5 tree item for populating a HDF5 Tree Widget
    Use .attrs dictionary to store useful information, such as dt
    """

    def __init__(self, parent=None):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.name = ''
        self.path = ''
        self.dataIndex = None
        self.originalIndex = None
        self.attrs = {}
        
    def set_name(self, name):
        self.name = name
        self.setText(0, self.name)

    def __lt__(self, otherItem):
        """ Reimplement sorting function to sort# numbers properly
        """
        column = self.treeWidget().sortColumn()
        try:
            return int(self.text(column).toLower()) < int(otherItem.text(column).toLower())
        except ValueError:
            return self.text(column).toLower() < otherItem.text(column).toLower()



class h5TreeWidget(QtGui.QTreeWidget):

    """ Reimplement QTreWidget Class
    
    Deals with Drag and Drop events by hacking some native methods:
    
    1) dropEvent emits SIGNAL 'dropped' when something has been dropped
    2) dropMimeData emits SIGNAL 'targetPosition' to output where the item 
    has been dropped  
     
    Transfer of the item(s) data is then dealt with by methods in the
    NeuroDaqWindow Class, which mantain and keep track of a database with 
    all the necessary data and properties.
    
    This is not the proper way of doing it. It would be best to reimplement
    all the main drag and drop methods and transfer the data across as MimeData.
    I've tried this and it works fine, but it was very clunky and would freeze
    by no apparent reason. This one is not pretty but works fine. 
    
    Allows for setting size hint
    h5TreeWidget(width, height, [parent=None])
    """

    def __init__(self, width, height, parent = None):
        QtGui.QTreeWidget.__init__(self, parent)  
        self.setAcceptDrops(True)
        self.dragData = None        
        self._width = width
        self._height = height
        #self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
                
    def dropEvent(self, event):   
        super(h5TreeWidget, self).dropEvent(event)
        if event.source() == self:
            pass
        else:
            self.emit(QtCore.SIGNAL('dropped'))
            
    def dropMimeData(self, parent, row, data, action):
        super(h5TreeWidget, self).dropMimeData(parent, row, data, action)
        self.emit(QtCore.SIGNAL('targetPosition'), parent, row)
        if action == QtCore.Qt.MoveAction:
            return True
        return False
                     
    def sizeHint(self):
        return QtCore.QSize(self._width, self._height)                     
                     


