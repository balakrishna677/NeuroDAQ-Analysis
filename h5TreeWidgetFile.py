import h5py
import sip

from PyQt4 import QtGui
from PyQt4 import QtCore

class h5Item(QtGui.QTreeWidgetItem):
    def __init__(self, parent=None):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        #super(DragableItem, self).__init__(parent)
        self.name = ''
        self.path = ''
        
    def set_name(self, name):
        self.name = name
        self.setText(0, self.name)


class h5TreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        QtGui.QTreeWidget.__init__(self, parent)  
        self.setAcceptDrops(True)
        self.dragData = None        
                
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
                     


