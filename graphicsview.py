from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Image
import ImageQt



class DesignerGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(DesignerGraphicsView, self).__init__(*args, **kwargs)
        scene = QGraphicsScene(self)
        self.scene = scene
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setCacheMode(QGraphicsView.CacheNone)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.selected = None
        self.grabbed = None

    def clear(self):
        self.scene.clear()
        self.scene.invalidate()

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton or mouseEvent.button() == Qt.RightButton:
            pos = self.mapToScene(mouseEvent.pos())
            items = self.scene.items(pos)
            if items:
                if mouseEvent.button() == Qt.LeftButton:
                    self.selected = items[0]
                    self.grabbed = self.selected
                else:
                    self.selected = items[0]
                    self.mainWindow.removeSelectedItem()
            else:
                point = self.mapToScene(mouseEvent.pos())
                x, y = self.gridify(point.x(), point.y())
                if self.mainWindow.tool:
                    self.addUnit(self.mainWindow.tool, x, y)

    def addUnit(self, tool, x, y):
        unit = self.mainWindow.getCurrentLayout().addUnit(self.mainWindow.tool.type, self.mainWindow.tool.name, x, y)
        if tool.type == 'sprite':
            item = QGraphicsPixmapItem(tool.pixmap)
            item.setOffset(x - tool.offsetX, y - tool.offsetY)
        else:
            raise Exception, 'Unknown tool type %s' %tool.type
        self.selected = item
        item.unit = unit
        item.tool = tool
        self.scene.addItem(item)

    def gridify(self, x, y):
        #TODO: add grid preference here
        gridStep = 0
        if not gridStep == 0:
            x = round(x/gridStep)*gridStep
            y = round(y/gridStep)*gridStep
        return x, y

    def mouseReleaseEvent(self, mouseEvent):
        if self.grabbed:
            point = self.mapToScene(mouseEvent.pos())
            x, y = self.gridify(point.x(), point.y())
            self.mainWindow.getCurrentLayout().moveUnit(self.grabbed, x, y, forceSave=True)
        self.grabbed = None

    def mouseMoveEvent(self, mouseEvent):
        if self.grabbed:
            point = self.mapToScene(mouseEvent.pos())
            x, y = self.gridify(point.x(), point.y())
            self.mainWindow.getCurrentLayout().moveUnit(self.grabbed, x, y, disableSave=True)
