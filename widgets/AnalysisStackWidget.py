from PyQt4 import QtGui, QtCore

class AnalysisStackWidget(QtGui.QStackedWidget):

    """ Reimplement QListView Class to allow setting a size hint.    
        AnalysisSelectWidget(width, height)
    """

    def __init__(self, width, height):
        QtGui.QStackedWidget.__init__(self)
        self._width = width
        self._height = height
        
    def sizeHint(self):
        return QtCore.QSize(self._width, self._height)




