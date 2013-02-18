#!/usr/bin/python
import os, sys
import functools
from copy import deepcopy
from pprint import pprint

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Image
import ImageQt

import const

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
        self.getCurrentLayout().show()

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
        self.unitsXComboBox.activated.connect(self.onUnitsXComboBoxChanged)
        self.unitsYComboBox.activated.connect(self.onUnitsYComboBoxChanged)

    def deselect(self):
        self.graphicsView.selected = None
        self.posXSpinBox.setValue(0)
        self.posYSpinBox.setValue(0)
        self.alignLeftRadio.setChecked(True)
        self.alignBottomRadio.setChecked(True)
        self.resourceIdEdit.setText('')
        self.resourceLabel.setText('')

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
        self.deselect()

    def onItemSelected(self, item):
        self.updateInfoBar(item)

    def updateInfoBar(self, item):
        self.resourceLabel.setText(item.name)
        self.posXSpinBox.setValue(item.prop[const.KEY_X])
        self.posYSpinBox.setValue(item.prop[const.KEY_Y])
        if item.prop[const.KEY_ALIGN_LEFT]:
            self.alignLeftRadio.setChecked(True)
        else:
            self.alignRightRadio.setChecked(True)
        if item.prop[const.KEY_ALIGN_BOTTOM]:
            self.alignBottomRadio.setChecked(True)
        else:
            self.alignTopRadio.setChecked(True)
        if item.prop[const.KEY_X_UNIT] == const.UNIT_PX:
            self.unitsXComboBox.setCurrentIndex(const.UNIT_PX_POS)
        else:
            self.unitsXComboBox.setCurrentIndex(const.UNIT_PERCENT_POS)
        if item.prop[const.KEY_Y_UNIT] == const.UNIT_PX:
            self.unitsYComboBox.setCurrentIndex(const.UNIT_PX_POS)
        else:
            self.unitsYComboBox.setCurrentIndex(const.UNIT_PERCENT_POS)

    @ifItemSelected
    def onAlignBottomRadioToggled(self, selectedItem, event):
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropAlignBottom(selectedItem, self.graphicsView.geometry().size(), mapPos, event)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onAlignLeftRadioToggled(self, selectedItem, event):
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropAlignLeft(selectedItem, self.graphicsView.geometry().size(), mapPos, event)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onPosXSpinBoxChanged(self, selectedItem):
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropPos(selectedItem, self.graphicsView.geometry().size(), mapPos)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onPosYSpinBoxChanged(self, selectedItem):
        print('onPoxYSpinBox changed')

    @ifItemSelected
    def onUnitsXComboBoxChanged(self, selectedItem, event):
        units = unicode(self.unitsXComboBox.currentText()).lower()
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropXUnit(selectedItem, self.graphicsView.geometry().size(), mapPos, units)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onUnitsYComboBoxChanged(self, selectedItem, event):
        units = unicode(self.unitsYComboBox.currentText()).lower()
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropYUnit(selectedItem, self.graphicsView.geometry().size(), mapPos, units)
        self.updateInfoBar(selectedItem)


class Layout(object):
    HISTORY_LEN = 20
    def __init__(self, mainWindow, d=None):
        self.current = 0#current frame in history
        self.mainWindow = mainWindow
        self.lastPropId = 0
        if d == None:
            self.d = {}
            self.d[const.KEY_PROPS] = []
            self.history = []
        else:
            self.d = d
            for prop in self.d.get(const.KEY_PROPS, []):
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
    def addProp(self, item):
        item.prop[const.KEY_ID] = self.incPropId()
        self.d[const.KEY_PROPS].append(item.prop)

    @saveHistory
    def removeProp(self, item):
        self.d[const.KEY_PROPS].remove(item.prop)

    @saveHistory
    def changePropPos(self, item, mapSize, mapPos):
        item.updatePropPos(mapSize, mapPos)

    @saveHistory
    def changePropAlignLeft(self, item, mapSize, mapPos, align):
        item.prop[const.KEY_ALIGN_LEFT] = align
        item.updatePropPos(mapSize, mapPos)

    @saveHistory
    def changePropAlignBottom(self, item, mapSize, mapPos, align):
        item.prop[const.KEY_ALIGN_BOTTOM] = align
        item.updatePropPos(mapSize, mapPos)

    @saveHistory
    def changePropXUnit(self, item, mapSize, mapPos, unit):
        item.prop[const.KEY_X_UNIT] = unit
        item.updatePropPos(mapSize, mapPos)

    @saveHistory
    def changePropYUnit(self, item, mapSize, mapPos, unit):
        item.prop[const.KEY_Y_UNIT] = unit
        item.updatePropPos(mapSize, mapPos)

    def undo(self):
        self.mainWindow.deselect()
        if self.current+1 >= len(self.history):
            print("There are no further actions")
        else:
            self.current += 1
            self.d = deepcopy(self.history[self.current])
            self.show()
            self.mainWindow.setWindowModified(True)

    def redo(self):
        self.mainWindow.deselect()
        if self.current > 0:
            self.current -= 1
            self.d = deepcopy(self.history[self.current])
            self.show()
            self.mainWindow.setWindowModified(True)
        else:
            print("There are no further actions")

    def show(self):
        self.mainWindow.graphicsView.clear()
        for prop in self.d[const.KEY_PROPS]:
            name = prop[const.KEY_NAME]
            type = prop[const.KEY_TYPE]
            itemFactory = self.mainWindow.getItemFactory(type, name)
            item = itemFactory.createGraphicsItem(prop)
            item.updateScenePos(self.mainWindow.graphicsView)
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

    def createGraphicsItem(self, prop):
        item = PixmapItem(self.name, self.pixmap, prop)
        return item


class PixmapItem(QGraphicsPixmapItem):
    def __init__(self, name, pixmap, prop):
        super(PixmapItem, self).__init__(pixmap)
        self.name = name
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.offsetX = self.pixmap().width()/2
        self.offsetY = self.pixmap().height()/2
        self.setOffset(-self.offsetX, -self.offsetY)
        self.prop = prop

    def updateScenePos(self, graphicsView):
        mapSize = graphicsView.geometry().size()
        if self.prop[const.KEY_X_UNIT] == const.UNIT_PX:
            alignedX = self.prop[const.KEY_X]
        else:
            alignedX = self.prop[const.KEY_X]*mapSize.width()/100
        if self.prop[const.KEY_Y_UNIT] == const.UNIT_PX:
            alignedY = self.prop[const.KEY_Y]
        else:
            alignedY = self.prop[const.KEY_Y]*mapSize.height()/100
        if self.prop[const.KEY_ALIGN_LEFT]:
            x = alignedX
        else:
            x = mapSize.width() - alignedX
        if self.prop[const.KEY_ALIGN_BOTTOM]:
            y = mapSize.height() - alignedY
        else:
            y = alignedY
        self.setPos(graphicsView.mapToScene(QPoint(x, y)))

    def updatePropPos(self, mapSize, mapPos):
        if self.prop[const.KEY_ALIGN_LEFT]:
            alignedX = mapPos.x()
        else:
            alignedX = mapSize.width() - mapPos.x()
        if self.prop[const.KEY_ALIGN_BOTTOM]:
            alignedY = mapSize.height() - mapPos.y()
        else:
            alignedY = mapPos.y()
        if self.prop[const.KEY_X_UNIT] == const.UNIT_PX:
            self.prop[const.KEY_X] = alignedX
        else:
            self.prop[const.KEY_X] = alignedX*100/mapSize.width()
        if self.prop[const.KEY_Y_UNIT] == const.UNIT_PX:
            self.prop[const.KEY_Y] = alignedY
        else:
            self.prop[const.KEY_Y] = alignedY*100/mapSize.height()


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    form.raise_()
    app.exec_()


if __name__ == '__main__':
    main()

