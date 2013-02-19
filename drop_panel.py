__author__ = 'alex'

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DropPanel(QFrame):
    def __init__(self, *args, **kwargs):
        super(DropPanel, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setAutoFillBackground( True )
        self.defaultColor = self.palette().color(self.backgroundRole())
        self.highlightColor = QColor( 255, 150, 150 )

    def dragEnterEvent(self, event):
        self.setBackgroundColor(self.highlightColor)
        event.accept()

    def dragLeaveEvent(self, event):
        self.setBackgroundColor(self.defaultColor)
        event.accept()

    def dropEvent(self, event):
        self.setBackgroundColor(self.defaultColor)
        event.accept()
        if self.mainWindow.grabbed:
            self.mainWindow.removeSelectedItem()
            self.mainWindow.grabbed = None

    def setBackgroundColor(self, color):
        palette = self.palette()
        palette.setColor( self.backgroundRole(), color)
        self.setPalette(palette)
