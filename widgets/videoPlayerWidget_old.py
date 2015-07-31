# Qt example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

import sys
import os
import user
import vlc
from PyQt4 import QtGui, QtCore
from widgets import *
import pyqtgraph as pg

class videoPlayerWidget(QtGui.QWidget):
    """A simple Media Player using VLC and Qt
    """ 

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)           
        # creating a basic vlc instance
        self.Instance = vlc.Instance()
        # creating an empty vlc media player
        self.MediaPlayer = self.Instance.media_player_new()
        self.createVideoUI()
        self.createPlotUI()
        self.createLayout()
        self.isPaused = False
        self.filename = None
        self.xmax = None


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
        self.VideoFrame = QtGui.QFrame()
        self.Palette = self.VideoFrame.palette()
        self.Palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.VideoFrame.setPalette(self.Palette)
        self.VideoFrame.setAutoFillBackground(True)

        self.PositionSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.PositionSlider.setToolTip("Position")
        self.PositionSlider.setMaximum(1000)
        self.connect(self.PositionSlider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.HButtonBox = QtGui.QHBoxLayout()
        self.PlayButton = QtGui.QPushButton("Play")
        self.HButtonBox.addWidget(self.PlayButton)
        self.connect(self.PlayButton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)

        self.StopButton = QtGui.QPushButton("Stop")
        self.HButtonBox.addWidget(self.StopButton)
        self.connect(self.StopButton, QtCore.SIGNAL("clicked()"),
                     self.Stop)

        self.UpdateButton = QtGui.QPushButton("Update Plot")
        self.UpdateButton.setCheckable(True)
        self.UpdateButton.setChecked(True)
        self.HButtonBox.addWidget(self.UpdateButton)

        self.HButtonBox.addStretch(1)
        self.VolumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.VolumeSlider.setMaximum(200)
        self.VolumeSlider.setValue(self.MediaPlayer.audio_get_volume())
        self.VolumeSlider.setToolTip("Volume")
        self.HButtonBox.addWidget(self.VolumeSlider)
        self.connect(self.VolumeSlider,
                     QtCore.SIGNAL("valueChanged(int)"),self.setVolume)

        self.VBoxLayout = QtGui.QVBoxLayout(self.videoWidget)
        self.VBoxLayout.addWidget(self.VideoFrame)
        self.VBoxLayout.addWidget(self.PositionSlider)
        self.VBoxLayout.addLayout(self.HButtonBox)

        #self.setLayout(self.VBoxLayout)

        #open = QtGui.QAction("&Open", self)
        #self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)

        self.Timer = QtCore.QTimer(self)
        self.Timer.setInterval(100)
        self.connect(self.Timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.MediaPlayer.is_playing():
            self.MediaPlayer.pause()
            self.PlayButton.setText("Play")
            self.isPaused = True
            print 'paused'
        else:
            if self.MediaPlayer.play() == -1:
                #self.OpenFile()
                return
            self.MediaPlayer.play()
            self.PlayButton.setText("Pause")
            self.Timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.MediaPlayer.stop()
        self.PlayButton.setText("Play")


    def OpenFile(self):
        """Open a media file in a MediaPlayer
        """
        if not self.filename:
            return

        # create the media
        self.Media = self.Instance.media_new(unicode(self.filename))
        # put the media in the media player
        self.MediaPlayer.set_media(self.Media)

        # parse the metadata of the file
        self.Media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.Media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform == "linux2": # for Linux using the X Server
            self.MediaPlayer.set_xwindow(self.VideoFrame.winId())
        elif sys.platform == "win32": # for Windows
            self.MediaPlayer.set_hwnd(self.VideoFrame.winId())
        elif sys.platform == "darwin": # for MacOS
            self.MediaPlayer.set_agl(self.VideoFrame.windId())
        #self.PlayPause()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.MediaPlayer.audio_set_volume(Volume)

    def setPosition(self, Position):
        """Set the video position
        """
        # setting the position to where the slider was dragged
        pos = Position/1000.0
        self.MediaPlayer.set_position(pos)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

        # Move the cursor in plotsWidget
        if self.xmax is not None:
            self.plotsWidget.cursor1.setValue(self.xmax*pos)
        else:
            self.plotsWidget.cursor1.setValue(Position)

    def cursorMoved(self):
        """Set video slider to the cursor position
        """
        xpos = self.plotsWidget.cursor1.getXPos() 
        if self.xmax is not None:
            pos = xpos/self.xmax 
            self.PositionSlider.setValue(float(pos)*1000)
            self.MediaPlayer.set_position(float(pos))        


    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        pos = self.MediaPlayer.get_position()
        self.PositionSlider.setValue(pos*1000)
        if self.UpdateButton.isChecked():
            if self.xmax is not None:
                self.plotsWidget.cursor1.setValue(self.xmax*pos)
            else:
                self.plotsWidget.cursor1.setValue(pos*1000)

        if not self.MediaPlayer.is_playing():
            # no need to call this function if nothing is played
            self.Timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()


