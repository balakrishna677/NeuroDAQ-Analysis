import h5py
import sip
import re

from PyQt4 import QtGui, QtCore


class h5Item(QtGui.QTreeWidgetItem):

    """ HDF5 tree item for populating a HDF5 Tree Widget
    Use .attrs dictionary to store useful information, such as dt
    """

    def __init__(self, parent=None):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.name = ''
        self.path = ''
        self.group = ''
        self.channel = ''
        self.listIndex = None
        self.originalIndex = None
        self.data = None
        self.attrs = {}
        self.attrs['dt'] = 1
        self.analysis = {}
        
    def set_name(self, name):
        self.name = name
        self.setText(0, self.name)

    def __lt__(self, otherItem):
        """ Reimplement sorting function to sort numbers properly
        """
        column = self.treeWidget().sortColumn()
        item1 = str(self.text(column)) #.toLower())
        item2 = str(otherItem.text(column)) #.toLower())
        
        # Check if there are numbers in both strings to be sorted
        s1 = re.search(r"\d+(\.\d+)?", item1)  # this returns numbers if they exist
        s2 = re.search(r"\d+(\.\d+)?", item2)
        if (bool(s1) & bool(s2)): 
            # Check if there is a mix of numbers and other characters
            base1 = item1.strip(s1.group()) 
            base2 = item2.strip(s2.group())
            if (bool(base1) & bool(base2)):
                if base1==base2:
                    # The basenames are the same, sort by numbers
                    return int(s1.group()) < int(s2.group())
                else:
                    # The basenames are different, sort by characters
                    return item1 < item2
            else:
                # Only one string has numbers and other characters, or both are numbers only
                try:
                    return int(item1) < int(item2)
                except ValueError:      
                    #print item1, item2, item1<item2   
                    return item1 < item2                             
        else:
            # There are no numbers (or only one string has a number)
            #print item1, item2, item1<item2 
            return item1 < item2


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
    I've tried this and it works fine, but it was clunky and would freeze
    by no apparent reason. This one is not pretty but works better. 
    
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
        modifiers = QtGui.QApplication.keyboardModifiers()
        #modifiers = event.keyboardModifiers()
        self.emit(QtCore.SIGNAL('dropped'), event.source(), modifiers)
            
    def dropMimeData(self, parent, row, data, action):
        super(h5TreeWidget, self).dropMimeData(parent, row, data, action)
        self.emit(QtCore.SIGNAL('targetPosition'), parent, row)
        if action == QtCore.Qt.MoveAction:
            return True
        return False                   
 
    def sizeHint(self):
        return QtCore.QSize(self._width, self._height)                     
                     
    def keyPressEvent(self, event):
        """ Specify some key press events.
        """
        super(h5TreeWidget, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete:
            self.emit(QtCore.SIGNAL('deletePressed'))


class h5itemSelect(QtGui.QDialog):

    """ Make a dialog box that displays a clone of workingDataTree
    for selecting a h5item for analysis
    """
    
    def __init__(self, tree, text, extendendSelection=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.tree = tree
        self.text = text
        self.extendendSelection = extendendSelection
        self.cloneTree()
        self.makeButtons()
        self.setProps()    

    def setProps(self):
        self.labelwidget = QtGui.QLabel(self.text)
        self.grid = QtGui.QGridLayout(self)
        self.grid.addWidget(self.labelwidget, 0,0,1,2) 
        self.grid.addWidget(self.clone, 1,0,1,2)
        self.grid.addWidget(self.Cancel_btn, 2,0)
        self.grid.addWidget(self.OK_btn, 2,1)
        self.clone.headerItem().setText(0, 'Available data')
        if self.extendendSelection:
            self.clone.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        #self.clone.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

    def cloneTree(self):
        self.clone = QtGui.QTreeWidget()
        root = self.tree.invisibleRootItem()
        cloneRoot = self.clone.invisibleRootItem()
        self.iterateTree(root, cloneRoot)  
        #self.clone.setParent(self)            

    def iterateTree(self, parent, cloneParent):
        for c in range(parent.childCount()):
            item = parent.child(c)
            itemName = item.text(0)
            cloneItem = QtGui.QTreeWidgetItem()
            cloneItem.setText(0, itemName)
            cloneParent.addChild(cloneItem)
            self.iterateTree(item, cloneItem) 
            
    def makeButtons(self):
        self.OK_btn = QtGui.QPushButton("OK", self)
        self.Cancel_btn = QtGui.QPushButton("Cancel", self)
        self.OK_btn.clicked.connect(self.accept)
        self.Cancel_btn.clicked.connect(self.reject)

    def getItemPath(self):
        try:
            item = self.clone.selectedItems()[0]
            path = []
            while item is not None:
                path.append(str(item.text(0)))
                item = item.parent()
            return '/'.join(reversed(path))
        except IndexError:
            self.reject()




            
            
