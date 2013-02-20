#!/usr/bin/python
import json
import logging
import os, sys
from copy import deepcopy
from pprint import pprint

import Image
import ImageQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import const
from designer_ui import Ui_MainWindow
from exporters import LuaExporter


def ifItemSelected(function):
    def newFunction(self, *args, **kwrags):
        if self.selected:
            return function(self, self.selected, *args, **kwrags)
    return newFunction


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.selectedItemFactory = None
        self.workingDir = None
        self.pixmapItemFactories = {}
        self.selected = None
        self.grabbed = None
        self.layoutPath = None
        self.currentFilePath = None

        self.graphicsView.mainWindow = self
        self.dropPanel.mainWindow = self
        self.graphicsView.scene.setSceneRect(QRectF(self.graphicsView.geometry()))
        self.connectSlots()
        self.layout = Layout(self)

    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        self.updateWindowTitle()

    def resizeEvent(self, evt=None):
        self.updateWindowTitle()
        self.getCurrentLayout().show()

    def updateWindowTitle(self):
        size = self.graphicsView.geometry().size()
        self.setWindowTitle("Size %sx%s" %(size.width(), size.height()))

    def clearProject(self):
        self.layout = Layout(self)
        self.graphicsView.clear()
        self.spritesListWidget.clear()
        self.pixmapItemFactories.clear()

    def getCurrentLayout(self):
        return self.layout

    def connectSlots(self):
        self.actionSet_Dir.triggered.connect(self.selectDir)
        def slot(item):
            self.selectedItemFactory = self.getPixmapItemFactory(item.name)
        self.spritesListWidget.itemPressed.connect(slot)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.alignBottomRadio.toggled.connect(self.onAlignBottomRadioToggled)
        self.alignLeftRadio.toggled.connect(self.onAlignLeftRadioToggled)
        self.posXSpinBox.editingFinished.connect(self.onPosXSpinBoxChanged)
        self.posYSpinBox.editingFinished.connect(self.onPosYSpinBoxChanged)
        self.unitsXComboBox.activated.connect(self.onUnitsXComboBoxChanged)
        self.unitsYComboBox.activated.connect(self.onUnitsYComboBoxChanged)
        self.actionNew.triggered.connect(self.newFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_As.triggered.connect(self.saveFileAs)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionExport_Layout.triggered.connect(self.exportLayout)
        self.workingDirToolButton.clicked.connect(self.selectDir)
        self.layoutPathToolButton.clicked.connect(self.selectLayoutPath)
        self.resourceIdEdit.textEdited.connect(self.onUidChanged)

    def deselect(self):
        self.selected = None
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

    def selectDir(self):
        dirPath=QFileDialog.getExistingDirectory(None, "Set Dir")
        if dirPath:
            self.setDirWithPath(dirPath)

    def selectLayoutPath(self):
        path=QFileDialog.getOpenFileName(None, "Select Layout Path")
        if path:
            self.setLayoutPath(path)
            return path

    def setLayoutPathLabelText(self, path):
        self.layoutPathLabel.setText(self.elided(path))
        self.layoutPathLabel.setToolTip(path)

    def setLayoutPath(self, path):
        path = unicode(path)
        self.layoutPath = path
        self.setLayoutPathLabelText(path)
        self.getCurrentLayout().setLayoutPath(path)

    def setWorkingDirLabelText(self, dirPath):
        self.workingDirLabel.setText(self.elided(dirPath))
        self.workingDirLabel.setToolTip(dirPath)

    def setDirWithPath(self, dirPath):
        self.clearProject()
        self.workingDir = unicode(dirPath)
        self.getCurrentLayout().setWorkingDir(dirPath)
        listDir = map(lambda x: os.path.join(self.workingDir, x), self.filteredListDir(dirPath))
        self.createPreviews(self.spritesListWidget, listDir, 120)
        self.setWorkingDirLabelText(dirPath)
        self.getCurrentLayout().toDict()[const.KEY_WORKING_DIR] = self.workingDir

    def filteredListDir(self, dirName):
        # remove Thumbs.db and hidden files from list
        return [f for f in os.listdir(dirName) if ((not f.startswith(".")) and (f.lower()[-4:] in ('.png', '.jpg')))]
        
    def getPixmapItemFactory(self, uniqueName):
        path = os.path.join(self.workingDir, uniqueName)
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
        self.selected = item
        self.updateInfoBar(item)

    def clearGrabbed(self):
        self.grabbed = None

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
        self.resourceIdEdit.setText(item.prop.get(const.KEY_UID, ''))

    @ifItemSelected
    def onAlignBottomRadioToggled(self, selectedItem, event):
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropAlignBottom(selectedItem, mapPos, event)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onAlignLeftRadioToggled(self, selectedItem, event):
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropAlignLeft(selectedItem, mapPos, event)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onPosXSpinBoxChanged(self, selectedItem):
        x = self.posXSpinBox.valueFromText(self.posXSpinBox.text())
        self.getCurrentLayout().changePropXPos(selectedItem, x)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onPosYSpinBoxChanged(self, selectedItem):
        y = self.posYSpinBox.valueFromText(self.posYSpinBox.text())
        self.getCurrentLayout().changePropYPos(selectedItem, y)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onUnitsXComboBoxChanged(self, selectedItem, event):
        units = unicode(self.unitsXComboBox.currentText()).lower()
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropXUnit(selectedItem, mapPos, units)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onUnitsYComboBoxChanged(self, selectedItem, event):
        units = unicode(self.unitsYComboBox.currentText()).lower()
        mapPos = self.graphicsView.mapFromScene(selectedItem.pos())
        self.getCurrentLayout().changePropYUnit(selectedItem, mapPos, units)
        self.updateInfoBar(selectedItem)

    @ifItemSelected
    def onUidChanged(self, selectedItem, event):
        self.getCurrentLayout().changePropUid(selectedItem, unicode(event))

    def newFile(self):
        self.currentFileName = None
        self.clearProject()

    def openFile(self):
        path=QFileDialog.getOpenFileName(None, "FileDialog")
        if path:
            with open(path) as f:
                self.currentFilePath = path
                self.loadFromString(f.read(), json)
                self.setWindowModified(False)

    def loadFromString(self, s, formatter):
        self.graphicsView.clear()
        try:
            d = formatter.loads(s)
        except Exception as e:
            logging.exception(e)
            d = {}
        if const.KEY_WORKING_DIR in d:
            self.setDirWithPath(d[const.KEY_WORKING_DIR])
        if const.KEY_LAYOUT_PATH in d:
            self.setLayoutPath(d[const.KEY_LAYOUT_PATH])
        self.layout = Layout(self, d)
        self.layout.show()

    def saveFile(self, formatter=None):
        if not formatter:
            formatter = json
        if self.currentFilePath:
            with open(self.currentFilePath, 'w') as f:
                f.write(formatter.dumps(self.getCurrentLayout().toDict()))
                self.setWindowModified(False)
        else:
            self.saveFileAs()

    def saveFileAs(self, *args, **kwargs):
        filename=QFileDialog.getSaveFileName(None, "FileDialog")
        if filename:
            self.currentFilePath = filename
            self.saveFile(*args, **kwargs)

    def exportLayout(self):
        layoutPath = self.getCurrentLayout().toDict().get(const.KEY_LAYOUT_PATH)
        if not layoutPath:
            layoutPath = self.selectLayoutPath()
        exporter = LuaExporter()
        if layoutPath:
            with open(layoutPath, 'w') as out:
                out.write(exporter.export(self.getCurrentLayout().toDict()))

    def elided(self, text, width=20):
        if len(text) > width:
            return '...%s' %text[-width+3:]
        else:
            return text


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

    def getMapSize(self):
        return self.mainWindow.graphicsView.geometry().size()

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
    def changePropUid(self, item, uid):
        item.prop[const.KEY_UID] = uid

    @saveHistory
    def removeProp(self, item):
        self.d[const.KEY_PROPS].remove(item.prop)

    @saveHistory
    def changePropPos(self, item, mapPos):
        item.updatePropPos(self.getMapSize(), mapPos)

    @saveHistory
    def changePropXPos(self, item, x):
        item.prop[const.KEY_X] = x
        item.updateScenePos(self.mainWindow.graphicsView)

    @saveHistory
    def changePropYPos(self, item, y):
        item.prop[const.KEY_Y] = y
        item.updateScenePos(self.mainWindow.graphicsView)

    @saveHistory
    def changePropAlignLeft(self, item, mapPos, align):
        item.prop[const.KEY_ALIGN_LEFT] = align
        item.updatePropPos(self.getMapSize(), mapPos)

    @saveHistory
    def changePropAlignBottom(self, item, mapPos, align):
        item.prop[const.KEY_ALIGN_BOTTOM] = align
        item.updatePropPos(self.getMapSize(), mapPos)

    @saveHistory
    def changePropXUnit(self, item, mapPos, unit):
        item.prop[const.KEY_X_UNIT] = unit
        item.updatePropPos(self.getMapSize(), mapPos)

    @saveHistory
    def changePropYUnit(self, item, mapPos, unit):
        item.prop[const.KEY_Y_UNIT] = unit
        item.updatePropPos(self.getMapSize(), mapPos)

    @saveHistory
    def setLayoutPath(self, layoutPath):
        self.d[const.KEY_LAYOUT_PATH] = layoutPath

    @saveHistory
    def setWorkingDir(self, dirPath):
        self.d[const.KEY_WORKING_DIR] = dirPath

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
            self.mainWindow.setWorkingDirLabelText(self.d.get(const.KEY_WORKING_DIR, const.PATH_NOT_SPECIFIED_TEXT))
            self.mainWindow.setLayoutPathLabelText(self.d.get(const.KEY_LAYOUT_PATH, const.PATH_NOT_SPECIFIED_TEXT))

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

