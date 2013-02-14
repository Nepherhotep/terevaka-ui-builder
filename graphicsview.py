from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Image
import ImageQt



class DesignerGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(DesignerGraphicsView, self).__init__(*args, **kwargs)
        self.setDragMode(QGraphicsView.RubberBandDrag)
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
                x, y = point.x(), point.y()
                if self.mainWindow.tool:
                    self.addUnit(self.mainWindow.tool, x, y)

    def addUnit(self, tool, x, y):
        unit = self.mainWindow.getCurrentLayout().addUnit(self.mainWindow.tool.type, self.mainWindow.tool.name, x, y)
        item = tool.createGraphicsItem(x, y)
        self.selected = item
        item.unit = unit
        item.tool = tool
        self.scene.addItem(item)