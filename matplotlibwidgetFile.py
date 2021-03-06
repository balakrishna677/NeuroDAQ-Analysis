from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
from matplotlib.figure import Figure
 
class mplCanvas(FigureCanvas): 
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.fig.set_facecolor('white')
 
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
 
class NavigationToolbar(NavigationToolbar2QTAgg):
    def __init__(self, canvas, parent, browser):
        NavigationToolbar2QTAgg.__init__(self,canvas,parent)
        for c in self.findChildren(QtGui.QToolButton):
            #print str(c.text())
            if str(c.text()) in ('Subplots','Customize','Back','Forward','Home'):
                c.defaultAction().setVisible(False)
        self.parent = parent
        self.browser = browser

    def zoom(self):
        super(NavigationToolbar, self).zoom(self)
        if self._active=="ZOOM":
            pass
        else:
            self.parent.cursor1.set_visible(False)
            self.parent.cursor2.set_visible(False)
            self.parent.canvas.draw()
            self.parent.background = self.parent.canvas.copy_from_bbox(self.parent.canvas.ax.bbox)
            if self.browser.ui.actionShowCursors.isChecked():
                self.parent.showCursorLastPos()
    
    def pan(self):
        super(NavigationToolbar, self).pan(self)
        if self._active=="PAN":
            pass
        else:
            self.parent.cursor1.set_visible(False)
            self.parent.cursor2.set_visible(False)
            self.parent.canvas.draw()
            self.parent.background = self.parent.canvas.copy_from_bbox(self.parent.canvas.ax.bbox)
            if self.browser.ui.actionShowCursors.isChecked():
                self.parent.showCursorLastPos()

    #def home(self):
    #    super(NavigationToolbar, self).home(self)
    #    self.parent.cursor1.set_visible(False)
    #    self.parent.cursor2.set_visible(False)
    #    self.parent.canvas.draw()
    #    self.parent.background = self.parent.canvas.copy_from_bbox(self.parent.canvas.ax.bbox)        
    #    if self.browser.ui.actionShowCursors.isChecked():
    #        self.parent.showCursorLastPos()            

class matplotlibWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)                        
        self.canvas = mplCanvas()
        #self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        #self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
        self.cursor1Pos = None
        self.cursor2Pos = None        

    def insertNavigationBar(self, browser):
        self.toolbar = NavigationToolbar(self.canvas, self, browser)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
    
    def createCursor(self):
        self.cursor1, = self.canvas.ax.plot([0],[0], 'r--', visible=False)
        self.cursor2, = self.canvas.ax.plot([0],[0], 'r--', visible=False)
        
    def initCursor(self):
        x1,x2,y1,y2 = self.canvas.ax.axis()
        self.cursor1Pos = x1+(x2-x1)/2.-(x2-x1)*0.2  # start cursors 20% from the midline 
        self.cursor2Pos = x1+(x2-x1)/2.+(x2-x1)*0.2 
        self.cursor1.set_data([self.cursor1Pos, self.cursor1Pos], [y1,y2])
        self.cursor1.set_visible(True)
        self.cursor2.set_data([self.cursor2Pos, self.cursor2Pos], [y1,y2])
        self.cursor2.set_visible(True)        
        self.blitCursors() 
    
    def hideCursor(self):
        self.cursor1.set_visible(False)
        self.cursor2.set_visible(False)    
        self.cursor1Pos = None
        self.cursor2Pos = None    
        self.blitCursors() 
        
    def showCursorLastPos(self):
        x1,x2,y1,y2 = self.canvas.ax.axis()
        self.cursor1.set_data([self.cursor1Pos, self.cursor1Pos], [y1,y2])         
        self.cursor2.set_data([self.cursor2Pos, self.cursor2Pos], [y1,y2]) 
        self.cursor1.set_visible(True)
        self.cursor2.set_visible(True)
        self.blitCursors() 
    
    def showCursor(self, event):
        x1,x2,y1,y2 = self.canvas.ax.axis()
        if event.inaxes==self.canvas.ax:
            selectionRange = (x2-x1)*0.05  # pick a cursor if mouse is within 5% of it (% of axis range)
            if (event.xdata > self.cursor1Pos-selectionRange) & (event.xdata < self.cursor1Pos+selectionRange):
                self.cursor1Pos = event.xdata
                self.cursor1.set_data([self.cursor1Pos, self.cursor1Pos], [y1,y2]) 
                self.cursor1.set_visible(True)
            elif (event.xdata > self.cursor2Pos-selectionRange) & (event.xdata < self.cursor2Pos+selectionRange):
                self.cursor2Pos = event.xdata
                self.cursor2.set_data([self.cursor2Pos, self.cursor2Pos], [y1,y2]) 
                self.cursor2.set_visible(True)          
            self.blitCursors()             
                        
    def refreshCursor(self, event): 
        x1,x2,y1,y2 = self.canvas.ax.axis()
        if self.cursor1Pos:
            self.cursor1.set_data([self.cursor1Pos, self.cursor1Pos], [y1,y2]) 
            self.cursor1.set_visible(True)
            self.cursor2.set_data([self.cursor2Pos, self.cursor2Pos], [y1,y2]) 
            self.cursor2.set_visible(True)             
        self.blitCursors() 
    
    def blitCursors(self):
        self.canvas.restore_region(self.background)
        self.canvas.ax.draw_artist(self.cursor1)
        self.canvas.ax.draw_artist(self.cursor2)
        self.canvas.blit(self.canvas.ax.bbox)      
        

