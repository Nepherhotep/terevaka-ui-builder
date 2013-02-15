#!/usr/bin/python
import os, sys
from copy import deepcopy

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Image
import ImageQt

from designer_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.graphicsView.mainWindow = self
        self.graphicsView.scene.setSceneRect(QRectF(self.graphicsView.geometry()))
        self.connectSlots()
        self.createEmptyLayout()
        self.tool = None
        self.spritesDir = None
        self.spriteTools = {}
        self.updateWindowTitle()
        self.setDirWithPath("./sprites")

    def updateWindowTitle(self):
        size = self.graphicsView.geometry().size()
        self.setWindowTitle("Size %sx%s" %(size.width(), size.height()))

    def createEmptyLayout(self):
        self.layout = Layout(self)

    def getCurrentLayout(self):
        return self.layout

    def connectSlots(self):
        self.connect(self.actionSet_Dir, SIGNAL('triggered()'), self.setDir)
        def slot(item):
            self.tool = self.getSpriteTool(item.name)
        self.spritesListWidget.itemClicked.connect(slot)
        self.connect(self.actionUndo, SIGNAL('triggered()'), self.undo)
        self.connect(self.actionRedo, SIGNAL('triggered()'), self.redo)

    def undo(self):
        self.getCurrentLayout().undo()

    def redo(self):
        self.getCurrentLayout().redo()

    def setDir(self):
        dirPath=QFileDialog.getExistingDirectory(None, "Set Dir", ".")
        if dirPath:
            self.setDirWithPath(dirPath)

    def setDirWithPath(self, dirPath):
        self.spritesDir = unicode(dirPath)
        listDir = map(lambda x: os.path.join(self.spritesDir, x), self.filteredListDir(dirPath))
        self.createPreviews(self.spritesListWidget, listDir, 120)

    def filteredListDir(self, dirName):
        # remove Thumbs.db and hidden files from list
        return [f for f in os.listdir(dirName) if ((not f.startswith(".")) and (f.lower()[-4:] in ('.png', '.jpg')))]
        
    def getSpriteTool(self, uniqueName):
        path = os.path.join(self.spritesDir, uniqueName)
        if path in self.spriteTools:
            return self.spriteTools[path]
        else:
            tool = SpriteTool(uniqueName, path)
            self.spriteTools[path] = tool
            return tool

    def getTool(self, toolType, name):
        if toolType == 'sprite':
            return self.getSpriteTool(name)
        else:
            raise Exception, "Unsupported tool type %s" %toolType

    def getCurrentLayout(self):
        return self.layout

    def createPreviews(self, listWidget, iconPathList, iconSize, thumbnail=False):
        listWidget.setIconSize(QSize(iconSize, iconSize))
        for path in sorted(iconPathList):
            picture = Image.open(path)
            if thumbnail:
                picture.thumbnail((thumbnail, thumbnail), Image.ANTIALIAS)
            try:
                icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
                filename = os.path.basename(path)
                if len(filename) <= 20:
                    label = filename
                else:
                    label = filename[:17] + "..."
                item = QListWidgetItem(label, listWidget)
                item.setIcon(icon)
                item.name = filename
                item.path = path
            except Exception, e:
                print(e, path)

    def removeSelectedItem(self):
        if self.graphicsView.selected:
            self.getCurrentLayout().removeUnit(self.graphicsView.selected)



class Layout(object):
    HISTORY_LEN = 20
    def __init__(self, mainWindow, d=None):
        self.current = 0#current frame in history
        self.mainWindow = mainWindow
        self.lastUnitId = 0
        if d == None:
            self.d = {}
            self.d['units'] = []
            self.history = []
        else:
            self.d = d
            for unit in self.d.get('units', []):
                self.incUnitId()
            self.history = [deepcopy(d)]

    def incUnitId(self):
        self.lastUnitId += 1
        return self.lastUnitId

    def saveHistory(function):
        def newFunction(self, *args, **kwargs):
            forceSave = kwargs.get('forceSave', False)
            disableSave = kwargs.get('disableSave', False)
            if disableSave:
                ans = function(self, *args, **kwargs)
            else:
                oldState = deepcopy(self.d)
                ans = function(self, *args, **kwargs)
                if forceSave or not oldState == self.d:
                    self.history = self.history[self.current:]
                    self.current = 0
                    self.history.insert(self.current, deepcopy(self.d))
                    if len(self.history) >= self.HISTORY_LEN:
                        self.history.pop()
                    self.mainWindow.setWindowModified(True)
            return ans
        return newFunction

    @saveHistory
    def addUnit(self, unittype, unitname, x, y):
        unit = {}
        unit['id'] = self.incUnitId()
        unit['type'] = unittype
        unit['name'] = unitname        
        unit['x'] = x
        unit['y'] = y
        self.d['units'].append(unit)
        return unit

    @saveHistory
    def removeUnit(self, item):
        self.d['units'].remove(item.unit)
        self.mainWindow.graphicsView.scene.removeItem(item)
        self.mainWindow.graphicsView.selected = None

    @saveHistory
    def moveUnit(self, item, x, y, **kwargs):
        item.setPos(x, y)
        item.unit['x'] = x
        item.unit['y'] = y

    def undo(self):
        self.mainWindow.graphicsView.selected = None
        if self.current+1 >= len(self.history):
            print("There are no further actions")
        else:
            self.current += 1
            self.d = deepcopy(self.history[self.current])
            self.show()
            self.mainWindow.setWindowModified(True)

    def redo(self):
        self.mainWindow.graphicsView.selected = None
        if self.current > 0:
            self.current -= 1
            self.d = deepcopy(self.history[self.current])
            self.show()
            self.mainWindow.setWindowModified(True)
        else:
            print("There are no further actions")

    def show(self):
        self.mainWindow.graphicsView.clear()
        for unit in self.d['units']:
            name = unit['name']
            type = unit['type']
            x = unit['x']
            y = unit['y']
            tool = self.mainWindow.getTool(type, name)
            item = tool.createGraphicsItem(x, y)
            item.unit = unit
            item.tool = tool
            self.mainWindow.graphicsView.scene.addItem(item)

    @saveHistory
    def setMsgOnStart(self, msg):
        if msg:
            self.d['start_msg'] = msg
        else:
            self.d.pop('start_msg', None)

    @saveHistory
    def setTimeLimit(self, limit):
        if limit:
            self.d['time_limit'] = limit
        else:
            self.d.pop('time_limit', None)

    def toDict(self):
        return self.d


class Tool(object):
    def __init__(self, toolType, name):
        self.name = name
        self.type = toolType

    def createGraphicsItem(self, x, y):
        raise NotImplementedError, "Subclass 'Tool' class and override this method"


class SpriteTool(Tool):
    def __init__(self, name, path, **params):
        self.name = name
        self.type = 'sprite'
        self.path = path
        picture = Image.open(path)
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(picture))
        self.offsetX = self.pixmap.width()/2
        self.offsetY = self.pixmap.height()/2
        for key, value in params.items():
            setattr(self, key, value)

    def createGraphicsItem(self, x, y):
        item = QGraphicsPixmapItem(self.pixmap)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        item.setOffset(-self.offsetX, -self.offsetY)
        item.setPos(QPointF(x, y))
        return item


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

