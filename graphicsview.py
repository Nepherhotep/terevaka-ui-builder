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
            self.mainWindow.onItemSelected(items[0])
            if mouseEvent.button() == Qt.LeftButton:
                self.mainWindow.grabbed = items[0]
                self.startDrag(mouseEvent, self.mainWindow.grabbed)

    def startDrag(self, mouseEvent, item):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(item.pixmap())
        standardOffset = QPoint(item.offsetX, item.offsetY)
        self.grabOffset = mouseEvent.pos() - self.mapFromScene(item.pos())
        drag.setHotSpot(standardOffset + self.grabOffset)
        drag.start(Qt.MoveAction)

    def addItem(self, itemFactory, posMap, posScene):
        prop = {}
        prop[const.KEY_TYPE] = self.mainWindow.selectedItemFactory.type
        prop[const.KEY_NAME] = self.mainWindow.selectedItemFactory.name

        #reset controls to default
        prop[const.KEY_ALIGN_LEFT] = True
        prop[const.KEY_ALIGN_BOTTOM] = True
        prop[const.KEY_X_UNIT] = const.UNIT_PX
        prop[const.KEY_Y_UNIT] = const.UNIT_PX

        item = itemFactory.createGraphicsItem(prop)
        #update pos according to selected controls
        item.updatePropPos(self.geometry(), posMap)
        item.updateScenePos(self)
        #save prop in layout
        self.mainWindow.getCurrentLayout().addProp(item)
        self.scene.addItem(item)
        self.mainWindow.onItemSelected(item)


