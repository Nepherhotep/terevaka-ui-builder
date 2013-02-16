#!/usr/bin/python
import os, sys
import functools
from copy import deepcopy
from pprint import pprint

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Image
import ImageQt

from designer_ui import Ui_MainWindow


def ifItemSelected(function):
    def newFunction(self, *args, **kwrags):
        if self.graphicsView.selected:
            return function(self, self.graphicsView.selected, *args, **kwrags)
    return newFunction


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.graphicsView.mainWindow = self
        self.graphicsView.scene.setSceneRect(QRectF(self.graphicsView.geometry()))
        self.connectSlots()
        self.createEmptyLayout()
        self.selectedItemFactory = None
        self.pixmapsDir = None
        self.pixmapItemFactories = {}
        self.setDirWithPath("./sprites")

    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        self.updateWindowTitle()

    def resizeEvent(self, evt=None):
        self.updateWindowTitle()

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
            self.selectedItemFactory = self.getPixmapItemFactory(item.name)
        self.spritesListWidget.itemPressed.connect(slot)
        self.connect(self.actionUndo, SIGNAL('triggered()'), self.undo)
        self.connect(self.actionRedo, SIGNAL('triggered()'), self.redo)
        self.alignBottomRadio.toggled.connect(self.onAlignBottomRadioToggled)
        self.alignLeftRadio.toggled.connect(self.onAlignLeftRadioToggled)
        self.posXSpinBox.editingFinished.connect(self.onPosXSpinBoxChanged)
        self.posYSpinBox.editingFinished.connect(self.onPosYSpinBoxChanged)

    def undo(self):
        self.getCurrentLayout().undo()

    def redo(self):
        self.getCurrentLayout().redo()

    def setDir(self):
        dirPath=QFileDialog.getExistingDirectory(None, "Set Dir", ".")
        if dirPath:
            self.setDirWithPath(dirPath)

    def setDirWithPath(self, dirPath):
        self.pixmapsDir = unicode(dirPath)
        listDir = map(lambda x: os.path.join(self.pixmapsDir, x), self.filteredListDir(dirPath))
        self.createPreviews(self.spritesListWidget, listDir, 120)

    def filteredListDir(self, dirName):
        # remove Thumbs.db and hidden files from list
        return [f for f in os.listdir(dirName) if ((not f.startswith(".")) and (f.lower()[-4:] in ('.png', '.jpg')))]
        
    def getPixmapItemFactory(self, uniqueName):
        path = os.path.join(self.pixmapsDir, uniqueName)
        if path in self.pixmapItemFactories:
            return self.pixmapItemFactories[path]
        else:
            itemFactory = PixmapItemFactory(uniqueName, path)
            self.pixmapItemFactories[path] = itemFactory
            return itemFactory

    def getItemFactory(self, itemFactoryType, name):
        if itemFactoryType == 'pixmap':
            return self.getPixmapItemFactory(name)
        else:
            raise Exception, "Unsupported itemFactoryTime type %s" %itemFactoryType

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

    @ifItemSelected
    def removeSelectedItem(self, selectedItem):
        self.getCurrentLayout().removeProp(selectedItem)
        self.graphicsView.scene.removeItem(selectedItem)
        self.graphicsView.selected = None

    def onItemSelected(self, item):
        self.updateInfoBar(item)

    def updateInfoBar(self, item):
        self.resourceLabel.setText(item.name)
        self.posXSpinBox.setValue(item.prop['x'])
        self.posYSpinBox.setValue(item.prop['y'])
        self.alignLeftRadio.setChecked(item.prop['align_left'])
        self.alignBottomRadio.setChecked(item.prop['align_bottom'])

    @ifItemSelected
    def onAlignBottomRadioToggled(self, selectedItem, event):
        selectedItem.prop['align_bottom'] = event
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        selectedItem.updatePos(self.graphicsView.size(), mapPos)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onAlignLeftRadioToggled(self, selectedItem, event):
        selectedItem.prop['align_left'] = event
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        selectedItem.updatePos(self.graphicsView.size(), mapPos)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onPosXSpinBoxChanged(self, selectedItem):
        if self.posXSpinBox.isActiveWindow():
            print('onPoxXSpinBox changed')

    @ifItemSelected
    def onPosYSpinBoxChanged(self, selectedItem):
        print('onPoxYSpinBox changed')



class Layout(object):
    HISTORY_LEN = 20
    def __init__(self, mainWindow, d=None):
        self.current = 0#current frame in history
        self.mainWindow = mainWindow
        self.lastPropId = 0
        if d == None:
            self.d = {}
            self.d['props'] = []
            self.history = []
        else:
            self.d = d
            for prop in self.d.get('props', []):
                self.incPropId()
            self.history = [deepcopy(d)]

    def incPropId(self):
        self.lastPropId += 1
        return self.lastPropId

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
    def addProp(self, prop):
        prop['id'] = self.incPropId()
        self.d['props'].append(prop)

    @saveHistory
    def removeProp(self, item):
        self.d['props'].remove(item.prop)

    @saveHistory
    def moveProp(self, prop, x, y):
        prop['x'] = x
        prop['y'] = y

    @saveHistory
    def changeLeftAlign(self, prop):
        pass

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
        for prop in self.d['props']:
            name = prop['name']
            type = prop['type']
            size = self.mainWindow.graphicsView.geometry().size()
            alignedX = prop['x']
            alignedY = prop['y']
            if prop['align_left']:
                x = alignedX
            else:
                x = size.width() - alignedX
            if prop['align_bottom']:
                y = size.height() - alignedY
            else:
                y = alignedY
            itemFactory = self.mainWindow.getItemFactory(type, name)
            posScene = self.mainWindow.graphicsView.mapToScene(QPoint(x, y))
            item = itemFactory.createGraphicsItem(posScene, prop)
            self.mainWindow.graphicsView.scene.addItem(item)

    def toDict(self):
        return self.d


class PixmapItemFactory(object):
    def __init__(self, name, path, **params):
        self.name = name
        self.type = 'pixmap'
        self.path = path
        picture = Image.open(path)
        self.pixmap = QPixmap.fromImage(ImageQt.ImageQt(picture))
        for key, value in params.items():
            setattr(self, key, value)

    def createGraphicsItem(self, posScene, prop):
        item = PixmapItem(self.name, self.pixmap, posScene, prop)
        return item


class PixmapItem(QGraphicsPixmapItem):
    def __init__(self, name, pixmap, pos, prop):
        super(PixmapItem, self).__init__(pixmap)
        self.name = name
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setPos(pos)
        self.offsetX = self.pixmap().width()/2
        self.offsetY = self.pixmap().height()/2
        self.setOffset(-self.offsetX, -self.offsetY)
        self.prop = prop

    def updatePos(self, mapSize, posMap):
        if self.prop['align_left']:
            self.prop['x'] = posMap.x()
        else:
            self.prop['x'] = mapSize.width() - posMap.x()
        if self.prop['align_bottom']:
            self.prop['y'] = mapSize.height() - posMap.y()
        else:
            self.prop['align_bottom'] = False
            self.prop['y'] = posMap.y()


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

