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

    def dropEvent(self, event):
        event.accept()
        if self.grabbed:
            self.grabbed.setPos(self.mapToScene(event.pos()))
            self.grabbed = None
        else:
            pos = self.mapToScene(event.pos())
            self.addUnit(self.mainWindow.tool, pos.x(), pos.y())
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
                self.startDrag(self.grabbed)

    def startDrag(self, item):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(item.tool.pixmap)
        drag.setHotSpot(QPoint(item.tool.offsetX, item.tool.offsetY))
        dropAction = drag.start(Qt.MoveAction)

    def addUnit(self, tool, x, y):
        unit = self.mainWindow.getCurrentLayout().addUnit(self.mainWindow.tool.type, self.mainWindow.tool.name, x, y)
        item = tool.createGraphicsItem(x, y)
        self.selected = item
        item.unit = unit
        item.tool = tool
        self.scene.addItem(item)


