from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

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
            
        

