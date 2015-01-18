from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

class plotWidget(pg.PlotWidget):

    """ Reimplement Pyqtgraph PlotWidget
    """
    
    def __init__(self, *args, **kwargs):
        pg.PlotWidget.__init__(self, *args, **kwargs)
        self.plotItem = self.getPlotItem()
        self.viewBox = self.plotItem.getViewBox()
        
    def keyPressEvent(self, event):
        """ Specify some key press events.
        """
        super(pg.PlotWidget, self).keyPressEvent(event)
        modifiers = QtGui.QApplication.keyboardModifiers()    
        
        # Zoom    
        if (event.key()==QtCore.Qt.Key_Right) and (modifiers==QtCore.Qt.ShiftModifier):
            self.viewBox.scaleBy(x=0.5, y=1)       
        elif (event.key()==QtCore.Qt.Key_Left) and (modifiers==QtCore.Qt.ShiftModifier):
            self.viewBox.scaleBy(x=2, y=1) 
        elif (event.key()==QtCore.Qt.Key_Up) and (modifiers==QtCore.Qt.ShiftModifier):
            self.viewBox.scaleBy(x=1, y=0.5)  
        elif (event.key()==QtCore.Qt.Key_Down) and (modifiers==QtCore.Qt.ShiftModifier):
            self.viewBox.scaleBy(x=1, y=2)  
        # Pan                                       
        elif event.key() == QtCore.Qt.Key_Right:        
            xRange = self.viewBox.viewRange()[0][1]-self.viewBox.viewRange()[0][0]
            self.viewBox.setXRange(self.viewBox.viewRange()[0][0]+xRange, self.viewBox.viewRange()[0][1]+xRange)
        elif event.key() == QtCore.Qt.Key_Left:        
            xRange = self.viewBox.viewRange()[0][1]-self.viewBox.viewRange()[0][0]
            self.viewBox.setXRange(self.viewBox.viewRange()[0][0]-xRange, self.viewBox.viewRange()[0][1]-xRange)
        elif event.key() == QtCore.Qt.Key_Down:
            yRange = (self.viewBox.viewRange()[1][1]-self.viewBox.viewRange()[1][0])/4.0
            self.viewBox.setYRange(self.viewBox.viewRange()[1][0]+yRange, self.viewBox.viewRange()[1][1]+yRange)
        elif event.key() == QtCore.Qt.Key_Up:
            yRange = (self.viewBox.viewRange()[1][1]-self.viewBox.viewRange()[1][0])/4.0
            self.viewBox.setYRange(self.viewBox.viewRange()[1][0]-yRange, self.viewBox.viewRange()[1][1]-yRange)

