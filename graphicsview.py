from PyQt4.QtCore import *
from PyQt4.QtGui import *

import const


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
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dragLeaveEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def onDragComplete(self, event):
        posMap = event.pos() - self.grabOffset
        self.mainWindow.grabbed.setPos(self.mapToScene(posMap))
        self.mainWindow.getCurrentLayout().changePropPos(self.mainWindow.grabbed, posMap)
        self.mainWindow.updateInfoBar(self.mainWindow.grabbed)

    def dropEvent(self, event):
        event.accept()
        if self.mainWindow.grabbed:
            self.onDragComplete(event)
            self.mainWindow.grabbed = None
        else:
            pos = self.mapToScene(event.pos())
            self.addItem(self.mainWindow.selectedItemFactory, event.pos(), pos)

    def clear(self):
        self.scene.clear()
        self.scene.invalidate()

    def mousePressEvent(self, mouseEvent):
        pos = self.mapToScene(mouseEvent.pos())
        items = self.scene.items(pos)
        if items:
            if hasattr(items[0], 'name'):
                self.mainWindow.onItemSelected(items[0])
                if mouseEvent.button() == Qt.LeftButton:
                    self.mainWindow.grabbed = items[0]
                    self.startDrag(mouseEvent, self.mainWindow.grabbed)

    def startDrag(self, mouseEvent, item):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = item.pixmap()
        scaleFactor = self.mainWindow.getScaleFactor()
        scaledPixmap = pixmap.scaledToWidth(pixmap.width() * scaleFactor)
        drag.setPixmap(scaledPixmap)
        standardOffset = QPoint(item.offsetX * scaleFactor, item.offsetY * scaleFactor)
        self.grabOffset = mouseEvent.pos() - self.mapFromScene(item.pos())
        drag.setHotSpot(standardOffset + self.grabOffset)
        drag.start(Qt.MoveAction)

    def addItem(self, itemFactory, posMap, posScene):
        prop = {}
        prop[const.KEY_TYPE] = self.mainWindow.selectedItemFactory.type
        prop[const.KEY_NAME] = self.mainWindow.selectedItemFactory.name

        #reset controls to default
        prop[const.KEY_HORIZONTAL_ALIGN] = const.ALIGN_CENTER
        prop[const.KEY_Z_INDEX] = 0

        item = itemFactory.createGraphicsItem(prop)
        #update pos according to selected controls
        item.scale(self.mainWindow.getScaleFactor(), self.mainWindow.getScaleFactor())
        item.updatePropPos(self.geometry(), posMap, self.mainWindow.getBaseSize(), self.mainWindow.getScaleFactor())
        item.updateScenePos(self, self.mainWindow.getBaseSize(), self.mainWindow.getScaleFactor())
        item.setZValue(prop[const.KEY_Z_INDEX])
        #save prop in layout
        self.mainWindow.getCurrentLayout().addProp(item)
        self.scene.addItem(item)
        self.mainWindow.onItemSelected(item)

    def drawRect(self, rect, bgColor = QColor(222, 255, 204), fgColor = QColor(0, 0, 0), z = 0):
        pen = QPen(fgColor)
        brush = QBrush(bgColor)
        rect = self.scene.addRect(rect, pen = pen, brush = brush)
        rect.setZValue(z)