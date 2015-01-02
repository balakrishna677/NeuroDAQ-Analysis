from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

class tableItem(QtGui.QTableWidgetItem):

    def __init__(self, parent=None):
        QtGui.QTableWidgetItem.__init__(self, parent)
        self.h5item = False
        self.h5link = ''

class TablePropsWidget(pg.TableWidget):

    """ Reimplement Pyqtgraph TableWidget Class to 
    catch some keyPresses
    """

    def __init__(self, *args, **kwargs):
        pg.TableWidget.__init__(self, *args, **kwargs)

    #def keyPressEvent(self, event):
    #    """ Emit SIGNAL to update H5 attribute on keypress
    #    """
    #    if event.key()==QtCore.Qt.Key_Enter or event.key()==QtCore.Qt.Key_Return:
            #print self.currentItem().text()
    #        self.emit(QtCore.SIGNAL('updateAttr'))
            # Currently only works for one property, dt            
            #attr = str(self.verticalHeaderItem(0).text())
            #attrValue = float(self.item(self.currentItem().row(), 0).text())
            #print self.verticalHeaderItem(0).text(), self.item(0,0).text()
            
        
class SpreadSheet2(QtGui.QMainWindow):

    def __init__(self, rows, cols, parent = None):
        super(SpreadSheet, self).__init__(parent)

        self.toolBar = QtGui.QToolBar()
        self.addToolBar(self.toolBar)
        self.formulaInput = QtGui.QLineEdit()
        #self.cellLabel = QtGui.QLabel(self.toolBar)
        #self.cellLabel.setMinimumSize(80, 0)
        #self.toolBar.addWidget(self.cellLabel)
        self.toolBar.addWidget(self.formulaInput)
        self.table = QtGui.QTableWidget(rows, cols, self)
        self.table.setDragEnabled(True)
        self.table.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.table.setDefaultDropAction(QtCore.Qt.MoveAction)
        #for c in range(cols):
        #    character = chr(ord('A') + c)
        #    self.table.setHorizontalHeaderItem(c, QtGui.QTableWidgetItem(character))

        #self.table.setItemPrototype(self.table.item(rows - 1, cols - 1))
        self.setCentralWidget(self.table)


        
class SpreadSheet(QtGui.QTableWidget):

    def __init__(self, rows, cols, parent = None):
        QtGui.QTableWidget.__init__(self, rows, cols, parent)  
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        for col in range(self.columnCount()):
            self.setColumnWidth(col,50)
            for row in range(self.rowCount()):            
                self.setRowHeight(row,20)
        

    def dropEvent(self, event):   
        super(SpreadSheet, self).dropEvent(event)
        modifiers = QtGui.QApplication.keyboardModifiers()
        #modifiers = event.keyboardModifiers()
        self.emit(QtCore.SIGNAL('droppedInTable'), event.source(), modifiers)
        print 'dropped', event.source()
            
    def dropMimeData(self, col, row, data, action):
        super(SpreadSheet, self).dropMimeData(row, col, data, action)
        self.emit(QtCore.SIGNAL('tableTargetPosition'), col, row)
        print row, col, action
        if action == QtCore.Qt.MoveAction:
            return True
        return False            


