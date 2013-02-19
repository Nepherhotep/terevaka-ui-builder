__author__ = 'alex'

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DropPanel(QFrame):
    def __init__(self, *args, **kwargs):
        super(DropPanel, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        print('drag enter event')
        event.accept()

    def dragLeaveEvent(self, event):
        print('drag leave event')
        event.accept()

    def dropEvent(self, event):
        event.accept()
        if self.mainWindow.graphicsView.grabbed:
            self.mainWindow.removeSelectedItem()
            self.mainWindow.graphicsView.grabbed = None
