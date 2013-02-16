from PyQt4.QtCore import *
from PyQt4.QtGui import *



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
        self.selected = None
        self.grabbed = None

    def dragEnterEvent(self, event):
        event.accept()

    def dragLeaveEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def onDragComplete(self, event):
        posMap = event.pos() - self.grabOffset
        self.grabbed.setPos(self.mapToScene(posMap))
        self.mainWindow.getCurrentLayout().moveProp(self.grabbed, self.geometry(), posMap)
        self.mainWindow.updateInfoBar(self.grabbed)

    def dropEvent(self, event):
        event.accept()
        if self.grabbed:
            self.onDragComplete(event)
            self.grabbed = None
        else:
            pos = self.mapToScene(event.pos())
            self.addItem(self.mainWindow.selectedItemFactory, event.pos(), pos)
            self.mainWindow.onItemSelected(self.selected)

    def clear(self):
        self.scene.clear()
        self.scene.invalidate()

    def mousePressEvent(self, mouseEvent):
        pos = self.mapToScene(mouseEvent.pos())
        items = self.scene.items(pos)
        if items:
            self.selected = items[0]
        if mouseEvent.button() == Qt.RightButton:
            if items:
                self.mainWindow.removeSelectedItem()
        else:
            if items:
                self.grabbed = self.selected
                self.mainWindow.onItemSelected(self.selected)
                self.startDrag(mouseEvent, self.grabbed)

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
        prop['type'] = self.mainWindow.selectedItemFactory.type
        prop['name'] = self.mainWindow.selectedItemFactory.name

        #reset controls to default
        self.mainWindow.alignBottomRadio.setChecked(True)
        self.mainWindow.alignLeftRadio.setChecked(True)
        prop['align_left'] = True
        prop['align_bottom'] = True

        #update pos according to selected controls
        item = itemFactory.createGraphicsItem(posScene, prop)
        item.updatePos(self.geometry(), posMap)
        self.mainWindow.getCurrentLayout().addProp(item)
        self.selected = item
        self.scene.addItem(item)



