from PyQt4 import QtGui, QtCore


class NeuroWidget(QtGui.QWidget):

    """ Reimplement QWidget Class to allow setting a size hint.    
        NeuroWidget(width, height)
    """

    def __init__(self, width, height):
        QtGui.QWidget.__init__(self)
        self._width = width
        self._height = height
        
    def sizeHint(self):
        return QtCore.QSize(self._width, self._height)
