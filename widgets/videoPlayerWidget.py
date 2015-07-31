import sys
import os
import user
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
from widgets import *
import pyqtgraph as pg
from moviepy.editor import *

class videoPlayerWidget(QtGui.QWidget):
    """A simple Media Player using Phonon
    """ 

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)           

        self.player = Phonon.VideoPlayer(Phonon.VideoCategory,self)
        self.createVideoUI()
        self.createPlotUI()
        self.createLayout()
        self.isPaused = False
        self.filename = None
        self.xmax = None
        self.nframes = None

    def createLayout(self):                  
        # Splitter
        self.gridLayout =  QtGui.QGridLayout(self)
        self.verticalsplitter = QtGui.QSplitter(self)
        self.verticalsplitter.setOrientation(QtCore.Qt.Vertical)
        self.gridLayout.addWidget(self.verticalsplitter, 0, 0, 1, 1)  

        # Add widgets       
        self.verticalsplitter.addWidget(self.videoWidget)
        self.verticalsplitter.addWidget(self.plotsWidget)
        self.verticalsplitter.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))
        self.verticalsplitter.setSizes([1,1]) 

           
    def createPlotUI(self):
        self.plotsWidget = plotWidget(background='#ECEDEB')
        self.plotsWidget.getAxis('bottom').setPen('k')
        self.plotsWidget.getAxis('left').setPen('k')        
        self.plotsWidget.showGrid(x=True, y=True, alpha=0.3) 
        self.plotsWidget.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))
        # cursor
        self.plotsWidget.cursor = True
        self.plotsWidget.cursor1 = pg.InfiniteLine(angle=90, movable=True, pen=pg.mkPen('#2AB825', width=2,))
        self.plotsWidget.addItem(self.plotsWidget.cursor1)
        self.plotsWidget.cursor1.sigPositionChanged.connect(self.cursorMoved)

    def createVideoUI(self):
        """Set up the user interface, signals & slots
        """

        # Video
        self.videoWidget = NeuroWidget(0,0)

        self.player.mediaObject().tick.connect(self.tock)
        self.player.mediaObject().setTickInterval(100)

        self.play_pause = QtGui.QPushButton("Play", self)
        self.play_pause.clicked.connect(self.playClicked)
        self.player.mediaObject().stateChanged.connect(self.stateChanged)

        self.PositionSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.PositionSlider.setToolTip("Position")
        #self.PositionSlider.setMaximum(1000)
        self.connect(self.PositionSlider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)
        #self.slider = Phonon.SeekSlider(self.player.mediaObject() , self)

        self.status = QtGui.QLabel(self)
        self.status.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignVCenter)

        self.VBoxLayout = QtGui.QVBoxLayout(self.videoWidget)
        self.VBoxLayout.addWidget(self.player)
        self.HButtonBox = QtGui.QHBoxLayout()
        self.HButtonBox.addWidget(self.play_pause)
        self.HButtonBox.addWidget(self.PositionSlider)
        self.HButtonBox.addWidget(self.status)
        self.VBoxLayout.addLayout(self.HButtonBox)

    def OpenFile(self):
        self.player.load(Phonon.MediaSource(self.filename))
        self.clip = VideoFileClip(self.filename)
        # set the slider maximum to number of frames
        #self.nframes = (self.player.mediaObject().totalTime()/1000.)*self.clip.fps     
        self.nframes = self.clip.duration*self.clip.fps
        self.PositionSlider.setMaximum(self.nframes)

    def playClicked(self):
        if self.player.mediaObject().state() == Phonon.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stateChanged(self, new, old):
        if new == Phonon.PlayingState:
            self.play_pause.setText("Pause")
        else:
            self.play_pause.setText("Play")

    def cursorMoved(self):
        """Set video slider to the cursor position
        """
        xpos = self.plotsWidget.cursor1.getXPos() 
        if self.xmax is not None:
            pos = xpos/self.xmax 
            self.PositionSlider.setValue(float(pos)*self.nframes)
            if not self.player.isPlaying():
                self.player.seek(float(pos*
                                 self.player.mediaObject().totalTime()))        


    def setPosition(self, Position):
        """Set the video position
        Position referes to the slider position and it is in frames
        Times in phonon are in ms.
        """
        t = Position/self.clip.fps*1000.
        self.player.seek(t)

        time = int(t)/1000
        h = time/3600
        m = (time-3600*h) / 60
        s = (time-3600*h-m*60)
        self.status.setText('%02d:%02d:%02d'%(h,m,s))

        # Move the cursor in plotsWidget
        if self.xmax is not None:
            pos = float(Position)/self.nframes * self.xmax
            self.plotsWidget.cursor1.setValue(pos)
        #else:
        #    self.plotsWidget.cursor1.setValue(Position)

    def tock(self, time):
        """ Updates items in the user interface as the movie plays
        """
        if self.player.isPlaying():
            self.PositionSlider.setValue((time/1000.)*self.clip.fps)
            if self.xmax is not None:
                pos = float(time)/self.player.mediaObject().totalTime()*self.xmax 
                self.plotsWidget.cursor1.setValue(pos)
        # Update timer    
        time = time/1000
        h = time/3600
        m = (time-3600*h) / 60
        s = (time-3600*h-m*60)
        self.status.setText('%02d:%02d:%02d'%(h,m,s))





