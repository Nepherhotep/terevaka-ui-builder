# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer.ui'
#
# Created: Thu Feb 14 12:29:54 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1126, 562)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.toolBox = QtGui.QToolBox(self.centralwidget)
        self.toolBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.toolBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.sprites = QtGui.QWidget()
        self.sprites.setGeometry(QtCore.QRect(0, 0, 200, 391))
        self.sprites.setObjectName(_fromUtf8("sprites"))
        self.spritesListWidget = QtGui.QListWidget(self.sprites)
        self.spritesListWidget.setGeometry(QtCore.QRect(10, 0, 181, 401))
        self.spritesListWidget.setViewMode(QtGui.QListView.IconMode)
        self.spritesListWidget.setObjectName(_fromUtf8("spritesListWidget"))
        self.toolBox.addItem(self.sprites, _fromUtf8(""))
        self.objects = QtGui.QWidget()
        self.objects.setGeometry(QtCore.QRect(0, 0, 200, 391))
        self.objects.setObjectName(_fromUtf8("objects"))
        self.objectsListWidget = QtGui.QListWidget(self.objects)
        self.objectsListWidget.setGeometry(QtCore.QRect(10, 0, 181, 401))
        self.objectsListWidget.setObjectName(_fromUtf8("objectsListWidget"))
        self.toolBox.addItem(self.objects, _fromUtf8(""))
        self.layout = QtGui.QWidget()
        self.layout.setGeometry(QtCore.QRect(0, 0, 200, 391))
        self.layout.setObjectName(_fromUtf8("layout"))
        self.layoutTreeWidget = QtGui.QTreeWidget(self.layout)
        self.layoutTreeWidget.setGeometry(QtCore.QRect(10, 0, 181, 381))
        self.layoutTreeWidget.setObjectName(_fromUtf8("layoutTreeWidget"))
        self.layoutTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.toolBox.addItem(self.layout, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.toolBox)
        self.graphicsView = DesignerGraphicsView(self.centralwidget)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(200, 0))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.unitsBox = QtGui.QGroupBox(self.frame)
        self.unitsBox.setGeometry(QtCore.QRect(10, 60, 181, 91))
        self.unitsBox.setObjectName(_fromUtf8("unitsBox"))
        self.percentButton = QtGui.QRadioButton(self.unitsBox)
        self.percentButton.setGeometry(QtCore.QRect(10, 60, 51, 20))
        self.percentButton.setObjectName(_fromUtf8("percentButton"))
        self.pxButton = QtGui.QRadioButton(self.unitsBox)
        self.pxButton.setGeometry(QtCore.QRect(10, 30, 51, 20))
        self.pxButton.setChecked(True)
        self.pxButton.setObjectName(_fromUtf8("pxButton"))
        self.horizontalAlignmentBox = QtGui.QGroupBox(self.frame)
        self.horizontalAlignmentBox.setGeometry(QtCore.QRect(10, 220, 181, 121))
        self.horizontalAlignmentBox.setObjectName(_fromUtf8("horizontalAlignmentBox"))
        self.alignLeftButton = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignLeftButton.setGeometry(QtCore.QRect(10, 30, 102, 20))
        self.alignLeftButton.setChecked(True)
        self.alignLeftButton.setObjectName(_fromUtf8("alignLeftButton"))
        self.alignRightButton = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignRightButton.setGeometry(QtCore.QRect(10, 60, 102, 20))
        self.alignRightButton.setObjectName(_fromUtf8("alignRightButton"))
        self.alignCenterButton = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignCenterButton.setGeometry(QtCore.QRect(10, 90, 102, 20))
        self.alignCenterButton.setObjectName(_fromUtf8("alignCenterButton"))
        self.verticalAlignmentBox = QtGui.QGroupBox(self.frame)
        self.verticalAlignmentBox.setGeometry(QtCore.QRect(10, 360, 181, 121))
        self.verticalAlignmentBox.setObjectName(_fromUtf8("verticalAlignmentBox"))
        self.alignCenterVerticalButton = QtGui.QRadioButton(self.verticalAlignmentBox)
        self.alignCenterVerticalButton.setGeometry(QtCore.QRect(10, 90, 102, 20))
        self.alignCenterVerticalButton.setObjectName(_fromUtf8("alignCenterVerticalButton"))
        self.alignBottomButton = QtGui.QRadioButton(self.verticalAlignmentBox)
        self.alignBottomButton.setGeometry(QtCore.QRect(10, 30, 102, 20))
        self.alignBottomButton.setChecked(True)
        self.alignBottomButton.setObjectName(_fromUtf8("alignBottomButton"))
        self.alignTopButton = QtGui.QRadioButton(self.verticalAlignmentBox)
        self.alignTopButton.setGeometry(QtCore.QRect(10, 60, 102, 20))
        self.alignTopButton.setObjectName(_fromUtf8("alignTopButton"))
        self.viewIdEdit = QtGui.QLineEdit(self.frame)
        self.viewIdEdit.setGeometry(QtCore.QRect(10, 30, 181, 22))
        self.viewIdEdit.setInputMask(_fromUtf8(""))
        self.viewIdEdit.setText(_fromUtf8(""))
        self.viewIdEdit.setPlaceholderText(_fromUtf8(""))
        self.viewIdEdit.setObjectName(_fromUtf8("viewIdEdit"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox.setGeometry(QtCore.QRect(10, 180, 81, 25))
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(110, 180, 81, 25))
        self.doubleSpinBox_2.setDecimals(1)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(30, 160, 16, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(130, 160, 16, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuResources = QtGui.QMenu(self.menubar)
        self.menuResources.setObjectName(_fromUtf8("menuResources"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionUndo = QtGui.QAction(MainWindow)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionSet_Dir = QtGui.QAction(MainWindow)
        self.actionSet_Dir.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.actionSet_Dir.setObjectName(_fromUtf8("actionSet_Dir"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionRedo = QtGui.QAction(MainWindow)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuResources.addAction(self.actionSet_Dir)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuResources.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.sprites), _translate("MainWindow", "Sprites", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.objects), _translate("MainWindow", "Objects", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.layout), _translate("MainWindow", "Layout", None))
        self.unitsBox.setTitle(_translate("MainWindow", "Positioning", None))
        self.percentButton.setText(_translate("MainWindow", "%", None))
        self.pxButton.setText(_translate("MainWindow", "Px", None))
        self.horizontalAlignmentBox.setTitle(_translate("MainWindow", "Horizontal Alignment", None))
        self.alignLeftButton.setText(_translate("MainWindow", "Left", None))
        self.alignRightButton.setText(_translate("MainWindow", "Right", None))
        self.alignCenterButton.setText(_translate("MainWindow", "Center", None))
        self.verticalAlignmentBox.setTitle(_translate("MainWindow", "Vertical Alignment", None))
        self.alignCenterVerticalButton.setText(_translate("MainWindow", "Center", None))
        self.alignBottomButton.setText(_translate("MainWindow", "Bottom", None))
        self.alignTopButton.setText(_translate("MainWindow", "Top", None))
        self.label.setText(_translate("MainWindow", "Sprite Id", None))
        self.label_2.setText(_translate("MainWindow", "X", None))
        self.label_3.setText(_translate("MainWindow", "Y", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuResources.setTitle(_translate("MainWindow", "Resources", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionUndo.setText(_translate("MainWindow", "Undo", None))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z", None))
        self.actionSet_Dir.setText(_translate("MainWindow", "Set Dir", None))
        self.actionSet_Dir.setShortcut(_translate("MainWindow", "Ctrl+D", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionRedo.setText(_translate("MainWindow", "Redo", None))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y", None))

from graphicsview import DesignerGraphicsView
