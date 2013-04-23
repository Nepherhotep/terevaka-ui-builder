#!/usr/bin/python
import json
import logging
import os, sys
from copy import deepcopy
from pprint import pprint

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
        self.layoutType = const.SCALABLE_LAYOUT_TYPE
        self.layoutPath = None
        self.currentFilePath = None

        self.graphicsView.mainWindow = self
        self.dropPanel.mainWindow = self
        self.connectSlots()
        self.layout = Layout(self)

    def drawBounds(self):
        sceneSize = self.graphicsView.geometry().size()
        baseSize = self.getBaseSize()
        rectWidth = float(baseSize.width())*sceneSize.height()/baseSize.height()
        offset = (sceneSize.width() - rectWidth)/2
        rect = QRectF(offset, 0, rectWidth, sceneSize.height())
        self.graphicsView.drawRect(rect)

    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        self.scaleGraphicsViewToContainer()
        self.graphicsView.scene.setSceneRect(QRectF(self.graphicsView.geometry()))
        self.updateWindowTitle()
        self.drawBounds()

    def resizeEvent(self, evt=None):
        self.updateWindowTitle()
        self.graphicsView.scene.setSceneRect(QRectF(self.graphicsView.geometry()))
        self.getCurrentLayout().updateUI()

    def updateWindowTitle(self):
        size = self.graphicsView.geometry().size()
        self.setWindowTitle("Size %sx%s" %(size.width(), size.height()))

    def clearProject(self):
        self.layout = Layout(self)
        self.graphicsView.clear()
        self.drawBounds()
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
        self.alignLeftRadio.clicked.connect(self.onHAlignRadioClicked)
        self.alignRightRadio.clicked.connect(self.onHAlignRadioClicked)
        self.alignCenterRadio.clicked.connect(self.onHAlignRadioClicked)
        self.posXSpinBox.editingFinished.connect(self.onPosXSpinBoxChanged)
        self.posYSpinBox.editingFinished.connect(self.onPosYSpinBoxChanged)
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
        self.alignCenterRadio.setChecked(True)
        self.resourceIdEdit.setText('')
        self.resourceLabel.setText('')

    def undo(self):
        self.getCurrentLayout().undo()

    def redo(self):
        self.getCurrentLayout().redo()

    @ifItemSelected
    def onHAlignRadioClicked(self, selectedItem, checked):
        if self.alignLeftRadio.isChecked():
            align = const.ALIGN_LEFT
        elif self.alignRightRadio.isChecked():
            align = const.ALIGN_RIGHT
        else:
            align = const.ALIGN_CENTER
        self.getCurrentLayout().changePropHAlign(selectedItem, align)
        self.getCurrentLayout().changePropPos(selectedItem, selectedItem.pos())
        self.updateInfoBar(selectedItem)

    def selectDir(self):
        dirPath=QFileDialog.getExistingDirectory(None, "Set Dir")
        if dirPath:
            self.setDirWithPath(dirPath)

    def selectLayoutPath(self):
        path=QFileDialog.getSaveFileName(None, "Select Layout Path")
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

    def scaleGraphicsViewToContainer(self):
        g = self.graphicsViewContainer.geometry()
        self.graphicsView.setGeometry(QRect(0, 0, g.width(), g.height()))

    def updateLayoutConfUI(self):
        self.scaleGraphicsViewToContainer()

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
        if itemFactoryType == 'sprite':
            return self.getPixmapItemFactory(name)
        else:
            raise Exception, "Unsupported itemFactoryTime type %s" %itemFactoryType

    def getCurrentLayout(self):
        return self.layout

    def createPreviews(self, listWidget, iconPathList, iconSize):
        listWidget.setIconSize(QSize(iconSize, iconSize))
        for path in sorted(iconPathList):
            try:
                icon = QIcon(QPixmap(path))
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
        if item.prop[const.KEY_HORIZONTAL_ALIGN] == const.ALIGN_LEFT:
            self.alignLeftRadio.setChecked(True)
        elif item.prop[const.KEY_HORIZONTAL_ALIGN] == const.ALIGN_RIGHT:
            self.alignRightRadio.setChecked(True)
        else:
            self.alignCenterRadio.setChecked(True)
        self.resourceIdEdit.setText(item.prop.get(const.KEY_UID, ''))

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
    def onUidChanged(self, selectedItem, event):
        self.getCurrentLayout().changePropUid(selectedItem, unicode(event))

    def newFile(self):
        self.currentFileName = None
        self.clearProject()

    def openFile(self, path=None):
        if not path:
            path=QFileDialog.getOpenFileName(None, "FileDialog")
        if path:
            path = unicode(path)
            os.chdir(os.path.dirname(path))
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
        self.layout.updateUI()

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
        filename = unicode(QFileDialog.getSaveFileName(None, "FileDialog"))
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

    def getBaseSize(self):
        width = self.layoutWidthSpinBox.valueFromText(self.layoutWidthSpinBox.text())
        height = self.layoutHeightSpinBox.valueFromText(self.layoutHeightSpinBox.text())
        return QSize(width, height)

    def getScaleFactor(self):
        return float(self.graphicsView.geometry().size().height())/self.getBaseSize().height()


class Layout(object):
    HISTORY_LEN = 20
    def __init__(self, mainWindow, d=None):
        self.current = 0#current frame in history
        self.mainWindow = mainWindow
        self.lastPropId = 0
        if d == None:
            self.d = {}
            self.d[const.KEY_PROPS] = []
            self.d[const.KEY_LAYOUT_TYPE] = const.SCALABLE_LAYOUT_TYPE
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
        item.updatePropPos(self.getMapSize(), mapPos, self.mainWindow.getBaseSize(), self.mainWindow.getScaleFactor())

    @saveHistory
    def changePropXPos(self, item, x):
        item.prop[const.KEY_X] = x
        item.updateScenePos(self.mainWindow.graphicsView, self.mainWindow.getBaseSize(), self.mainWindow.getScaleFactor())

    @saveHistory
    def changePropYPos(self, item, y):
        item.prop[const.KEY_Y] = y
        item.updateScenePos(self.mainWindow.graphicsView, self.mainWindow.getBaseSize(), self.mainWindow.getScaleFactor())

    @saveHistory
    def changePropHAlign(self, item, align):
        item.prop[const.KEY_HORIZONTAL_ALIGN] = align

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
            self.updateUI()
            self.mainWindow.setWindowModified(True)

    def redo(self):
        self.mainWindow.deselect()
        if self.current > 0:
            self.current -= 1
            self.d = deepcopy(self.history[self.current])
            self.updateUI()
            self.mainWindow.setWindowModified(True)
        else:
            print("There are no further actions")

    def updateUI(self):
        self.mainWindow.updateLayoutConfUI()
        self.mainWindow.graphicsView.clear()
        self.mainWindow.drawBounds()
        for prop in self.d[const.KEY_PROPS]:
            name = prop[const.KEY_NAME]
            type = prop[const.KEY_TYPE]
            itemFactory = self.mainWindow.getItemFactory(type, name)
            item = itemFactory.createGraphicsItem(prop)
            item.updateScenePos(self.mainWindow.graphicsView, self.mainWindow.getBaseSize(), self.mainWindow.getScaleFactor())
            item.scale(self.mainWindow.getScaleFactor(), self.mainWindow.getScaleFactor())
            self.mainWindow.graphicsView.scene.addItem(item)
        self.mainWindow.setWorkingDirLabelText(self.d.get(const.KEY_WORKING_DIR, const.PATH_NOT_SPECIFIED_TEXT))
        self.mainWindow.setLayoutPathLabelText(self.d.get(const.KEY_LAYOUT_PATH, const.PATH_NOT_SPECIFIED_TEXT))
        self.mainWindow.updateWindowTitle()

    def toDict(self):
        exportDict = deepcopy(self.d)
        #recalc path to relative
        if self.mainWindow.currentFilePath:
            currentPath = os.path.dirname(self.mainWindow.currentFilePath)
            if const.KEY_WORKING_DIR in exportDict:
                workingDir = unicode(exportDict[const.KEY_WORKING_DIR])
                exportDict[const.KEY_WORKING_DIR] = os.path.relpath(workingDir, currentPath)
            if const.KEY_LAYOUT_PATH in exportDict:
                layoutPath = unicode(exportDict[const.KEY_LAYOUT_PATH])
                exportDict[const.KEY_LAYOUT_PATH] = os.path.relpath(layoutPath, currentPath)
        return exportDict


class PixmapItemFactory(object):
    def __init__(self, name, path, **params):
        self.name = name
        self.type = 'sprite'
        self.path = path
        self.pixmap = QPixmap(path)
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

    def updateScenePos(self, graphicsView, baseSize, scaleFactor):
        mapSize = graphicsView.geometry().size()
        propPosX = self.prop[const.KEY_X]
        propPosY = self.prop[const.KEY_Y]
        offset = mapSize.width() - mapSize.height() * baseSize.width() / baseSize.height()
        if self.prop[const.KEY_HORIZONTAL_ALIGN] == const.ALIGN_LEFT:
            x = propPosX * scaleFactor
        elif self.prop[const.KEY_HORIZONTAL_ALIGN] == const.ALIGN_RIGHT:
            x = propPosX * scaleFactor + offset
        else:
            x = propPosX * scaleFactor + offset / 2
        y = mapSize.height() * ( 1 - float(propPosY) /baseSize.height())
        self.setPos(graphicsView.mapToScene(QPoint(x, y)))

    def updatePropPos(self, mapSize, mapPos, baseSize, scaleFactor):
        offset = mapSize.width() - mapSize.height() * baseSize.width() / baseSize.height()
        if self.prop[const.KEY_HORIZONTAL_ALIGN] == const.ALIGN_LEFT:
            alignedX = mapPos.x() / scaleFactor
        elif self.prop[const.KEY_HORIZONTAL_ALIGN] == const.ALIGN_RIGHT:
            alignedX = (mapPos.x() - offset ) / scaleFactor
        else:
            alignedX = (mapPos.x() - offset / 2) / scaleFactor

        alignedY =  (mapSize.height() - mapPos.y()) * float(baseSize.height())/mapSize.height()
        self.prop[const.KEY_X] = alignedX
        self.prop[const.KEY_Y] = alignedY



def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    form.raise_()
    if len(sys.argv) > 1:
        form.openFile(sys.argv[1])
    app.exec_()


if __name__ == '__main__':
    main()

