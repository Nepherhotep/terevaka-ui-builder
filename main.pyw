#!/usr/bin/python
import os, sys

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
        self.connectSlots()
        self.createEmptyLayer()
        self.tool = None
        self.dirs = []
        self.spriteTools = {}

    def createEmptyLayer(self):
        self.layer = Layer(self)

    def getCurrentLayer(self):
        return self.layer

    def connectSlots(self):
        self.connect(self.actionAdd_Dir, SIGNAL('triggered()'), self.addDir)
        def slot(item):
            self.tool = self.getTool(item.name, item.path)
        self.spritesListWidget.itemClicked.connect(slot)

    def addDir(self):
        dirName=QFileDialog.getExistingDirectory(None, "Add Dir", ".")
        if dirName:
            self.dirs.append(dirName)
            listDir = map(lambda x: os.path.join(unicode(dirName), x), self.filteredListDir(dirName))
            self.createPreviews(self.spritesListWidget, listDir, 120)

    def filteredListDir(self, dirName):
        # remove Thumbs.db and hidden files from list
        return [f for f in os.listdir(dirName) if ((not f.startswith(".")) and (f.lower()[-4:] in ('.png', '.jpg')))]
        
    def getTool(self, name, path):
        if path in self.spriteTools:
            return self.spriteTools[path]
        else:
            picture = Image.open(path)
            pixmap = QPixmap.fromImage(ImageQt.ImageQt(picture))
            tool = Tool(name, path, pixmap)
            self.spriteTools[path] = tool
            return tool

    def getCurrentLayer(self):
        return self.layer

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
                item.name = label
                item.path = path
            except Exception, e:
                print(e, path)


class Layer(object):
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
        tool = self.mainWindow.getTool(unittype, unitname)
        item = QGraphicsPixmapItem(tool.pixmap)
        item.setOffset(x - tool.offsetX, y - tool.offsetY)
        self.mainWindow.graphicsView.selected = item

        self.mainWindow.graphicsView.scene.addItem(item)
        unit = {}
        unit['id'] = self.incUnitId()
        unit['type'] = unittype
        unit['name'] = unitname        
        unit['x'] = x
        unit['y'] = y
        item.unit = unit
        self.d['units'].append(unit)

    @saveHistory
    def removeUnit(self, item):
        self.d['units'].remove(item.unit)
        self.mainWindow.graphicsView.scene.removeItem(item)
        self.mainWindow.graphicsView.selected = None

    @saveHistory
    def moveUnit(self, item, x, y, **kwargs):
        unittype = item.unit['type']
        unitname = item.unit['name']
        tool = self.mainWindow.getTool(unittype, unitname)
        item.setOffset(x - tool.offsetX, y - tool.offsetY)
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
            unitname = unit['name']
            unittype = unit['type']
            x = unit['x']
            y = unit['y']
            tool = self.mainWindow.getTool(unittype, unitname)
            item = QGraphicsPixmapItem(tool.pixmap)
            item.setOffset(x - tool.offsetX, y - tool.offsetY)
            item.unit = unit
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
    def __init__(self, name, path, pixmap, **params):
        self.name = name
        self.path = path
        self.pixmap = pixmap
        self.offsetX = pixmap.width()/2
        self.offsetY = pixmap.height()/2
        for key, value in params.items():
            setattr(self, key, value)


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

