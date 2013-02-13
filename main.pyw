#!/usr/bin/python
import os, sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Image
import ImageQt

from designer_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.connectSlots()
        self.dirs = []
        self.spriteTools = {}

    def connectSlots(self):
        self.connect(self.actionAdd_Dir, SIGNAL('triggered()'), self.addDir)
        def slot(item):
            self.tool = self.getTool(item.name, item.path)
        self.spritesListWidget.itemClicked.connect(slot)

    def addDir(self):
        dirName=QFileDialog.getExistingDirectory(None, "Add Dir", ".")
        if dirName:
            self.dirs.append(dirName)
            listDir = map(lambda x: os.path.join(unicode(dirName), x), self.filteredListDir(dirName))
            self.createPreviews(self.spritesListWidget, listDir, 120)

    def filteredListDir(self, dirName):
        # remove Thumbs.db and hidden files from list
        return [f for f in os.listdir(dirName) if ((not f.startswith(".")) and (f.lower()[-4:] in ('.png', '.jpg')))]
        
    def getTool(self, name, path):
        if path in self.spriteTools:
            return self.spriteTools[path]
        else:
            picture = Image.open(path)
            pixmap = QPixmap.fromImage(ImageQt.ImageQt(picture))
            tool = Tool(name, path, pixmap)
            self.spriteTools[path] = tool
            return tool

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
                item.name = label
                item.path = path
            except Exception, e:
                print(e, path)


class Tool(object):
    def __init__(self, name, path, pixmap, **params):
        self.name = name
        self.path = path
        self.pixmap = pixmap
        self.offsetX = pixmap.width()/2
        self.offsetY = pixmap.height()/2
        for key, value in params.items():
            setattr(self, key, value)


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

