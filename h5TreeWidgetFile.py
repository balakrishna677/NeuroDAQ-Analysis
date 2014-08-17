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
        self.dataIndex = None
        self.originalIndex = None
        
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
                     








   
class h5TreeWidgetTEST(QtGui.QTreeWidget):
# from http://www.riverbankcomputing.com/pipermail/pyqt/2009-December/025379.html
     def __init__(self, parent=None):
         QtGui.QTreeWidget.__init__(self, parent)
         self.header().setHidden(True)
         self.setSelectionMode(self.ExtendedSelection)
         #self.setDragDropMode(self.InternalMove)
         self.setDragEnabled(True)
         self.setDropIndicatorShown(True)

     def dropEvent(self, event):
         if event.source() == self:
             QtGui.QAbstractItemView.dropEvent(self, event)

     def dropMimeData(self, parent, row, data, action):
         if action == QtCore.Qt.MoveAction:
             return self.moveSelection(parent, row)
         return False

     def moveSelection(self, parent, position):
	# save the selected items
         selection = [QtCore.QPersistentModelIndex(i)
                      for i in self.selectedIndexes()]
         parent_index = self.indexFromItem(parent)
         if parent_index in selection:
             return False
         # save the drop location in case it gets moved
         target = self.model().index(position, 0, parent_index).row()
         if target < 0:
             target = position
         # remove the selected items
         taken = []
         for index in reversed(selection):
             item = self.itemFromIndex(QtCore.QModelIndex(index))
             if item is None or item.parent() is None:
                 taken.append(self.takeTopLevelItem(index.row()))
             else:
                 taken.append(item.parent().takeChild(index.row()))
         # insert the selected items at their new positions
         while taken:
             if position == -1:
                 # append the items if position not specified
                 if parent_index.isValid():
                     parent.insertChild(
                         parent.childCount(), taken.pop(0))
                 else:
                     self.insertTopLevelItem(
                         self.topLevelItemCount(), taken.pop(0))
             else:
		# insert the items at the specified position
                 if parent_index.isValid():
                     parent.insertChild(min(target,
                         parent.childCount()), taken.pop(0))
                 else:
                     self.insertTopLevelItem(min(target,
                         self.topLevelItemCount()), taken.pop(0))
                     
         return True


# copy across and move internally
# copy children
# copy whole selection > have to create a list with QStringList for data pack/unpack

