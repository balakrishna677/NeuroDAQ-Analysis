from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

class TablePropsWidget(pg.TableWidget):

    """ Reimplement Pyqtgraph TableWidget Class to 
    catch some keyPresses
    """

    def __init__(self, *args, **kwargs):
        pg.TableWidget.__init__(self, *args, **kwargs)

    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Enter or event.key()==QtCore.Qt.Key_Return:            
            attr = self.item(self.currentItem().row(), 0).text()
            print self.item(0,0).text(), self.item(0,1).text()
            
        

