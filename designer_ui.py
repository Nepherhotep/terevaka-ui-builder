# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer.ui'
#
# Created: Fri Feb 15 11:13:54 2013
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
        MainWindow.resize(1096, 526)
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
        self.sprites.setGeometry(QtCore.QRect(0, 0, 200, 355))
        self.sprites.setObjectName(_fromUtf8("sprites"))
        self.spritesListWidget = QtGui.QListWidget(self.sprites)
        self.spritesListWidget.setGeometry(QtCore.QRect(10, 0, 181, 401))
        self.spritesListWidget.setViewMode(QtGui.QListView.IconMode)
        self.spritesListWidget.setObjectName(_fromUtf8("spritesListWidget"))
        self.toolBox.addItem(self.sprites, _fromUtf8(""))
        self.objects = QtGui.QWidget()
        self.objects.setGeometry(QtCore.QRect(0, 0, 200, 355))
        self.objects.setObjectName(_fromUtf8("objects"))
        self.objectsListWidget = QtGui.QListWidget(self.objects)
        self.objectsListWidget.setGeometry(QtCore.QRect(10, 0, 181, 401))
        self.objectsListWidget.setObjectName(_fromUtf8("objectsListWidget"))
        self.toolBox.addItem(self.objects, _fromUtf8(""))
        self.layout = QtGui.QWidget()
        self.layout.setGeometry(QtCore.QRect(0, 0, 200, 355))
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
        self.resourceIdEdit = QtGui.QLineEdit(self.frame)
        self.resourceIdEdit.setGeometry(QtCore.QRect(30, 40, 161, 22))
        self.resourceIdEdit.setInputMask(_fromUtf8(""))
        self.resourceIdEdit.setText(_fromUtf8(""))
        self.resourceIdEdit.setPlaceholderText(_fromUtf8(""))
        self.resourceIdEdit.setObjectName(_fromUtf8("resourceIdEdit"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 42, 21, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 80, 181, 201))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.posXSpinBox = QtGui.QDoubleSpinBox(self.frame_2)
        self.posXSpinBox.setGeometry(QtCore.QRect(20, 20, 81, 25))
        self.posXSpinBox.setDecimals(2)
        self.posXSpinBox.setObjectName(_fromUtf8("posXSpinBox"))
        self.unitsXComboBox = QtGui.QComboBox(self.frame_2)
        self.unitsXComboBox.setGeometry(QtCore.QRect(110, 20, 61, 26))
        self.unitsXComboBox.setObjectName(_fromUtf8("unitsXComboBox"))
        self.unitsXComboBox.addItem(_fromUtf8(""))
        self.unitsXComboBox.addItem(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(7, 22, 16, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.posYSpinBox = QtGui.QDoubleSpinBox(self.frame_2)
        self.posYSpinBox.setGeometry(QtCore.QRect(20, 50, 81, 25))
        self.posYSpinBox.setDecimals(2)
        self.posYSpinBox.setObjectName(_fromUtf8("posYSpinBox"))
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(7, 52, 16, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.unitsYComboBox = QtGui.QComboBox(self.frame_2)
        self.unitsYComboBox.setGeometry(QtCore.QRect(110, 50, 61, 26))
        self.unitsYComboBox.setObjectName(_fromUtf8("unitsYComboBox"))
        self.unitsYComboBox.addItem(_fromUtf8(""))
        self.unitsYComboBox.addItem(_fromUtf8(""))
        self.label_5 = QtGui.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(21, 0, 141, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalAlignmentBox = QtGui.QGroupBox(self.frame_2)
        self.horizontalAlignmentBox.setGeometry(QtCore.QRect(10, 100, 71, 91))
        self.horizontalAlignmentBox.setObjectName(_fromUtf8("horizontalAlignmentBox"))
        self.alignLeftRadio = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignLeftRadio.setGeometry(QtCore.QRect(10, 30, 61, 20))
        self.alignLeftRadio.setChecked(True)
        self.alignLeftRadio.setObjectName(_fromUtf8("alignLeftRadio"))
        self.alignRightRadio = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignRightRadio.setGeometry(QtCore.QRect(10, 60, 61, 20))
        self.alignRightRadio.setObjectName(_fromUtf8("alignRightRadio"))
        self.verticalAlignmentBox = QtGui.QGroupBox(self.frame_2)
        self.verticalAlignmentBox.setGeometry(QtCore.QRect(100, 100, 71, 91))
        self.verticalAlignmentBox.setObjectName(_fromUtf8("verticalAlignmentBox"))
        self.alignBottomRadio = QtGui.QRadioButton(self.verticalAlignmentBox)
        self.alignBottomRadio.setGeometry(QtCore.QRect(10, 30, 71, 20))
        self.alignBottomRadio.setChecked(True)
        self.alignBottomRadio.setObjectName(_fromUtf8("alignBottomRadio"))
        self.alignTopRadio = QtGui.QRadioButton(self.verticalAlignmentBox)
        self.alignTopRadio.setGeometry(QtCore.QRect(10, 60, 61, 20))
        self.alignTopRadio.setObjectName(_fromUtf8("alignTopRadio"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(20, 90, 131, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.frame_3 = QtGui.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(10, 300, 181, 91))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.sizeWidthSpinBox = QtGui.QDoubleSpinBox(self.frame_3)
        self.sizeWidthSpinBox.setGeometry(QtCore.QRect(20, 20, 81, 25))
        self.sizeWidthSpinBox.setDecimals(2)
        self.sizeWidthSpinBox.setObjectName(_fromUtf8("sizeWidthSpinBox"))
        self.unitsWidthComboBox = QtGui.QComboBox(self.frame_3)
        self.unitsWidthComboBox.setGeometry(QtCore.QRect(110, 20, 61, 26))
        self.unitsWidthComboBox.setObjectName(_fromUtf8("unitsWidthComboBox"))
        self.unitsWidthComboBox.addItem(_fromUtf8(""))
        self.unitsWidthComboBox.addItem(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(self.frame_3)
        self.label_6.setGeometry(QtCore.QRect(7, 20, 16, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.sizeHeightSpinBox = QtGui.QDoubleSpinBox(self.frame_3)
        self.sizeHeightSpinBox.setGeometry(QtCore.QRect(20, 50, 81, 25))
        self.sizeHeightSpinBox.setDecimals(2)
        self.sizeHeightSpinBox.setObjectName(_fromUtf8("sizeHeightSpinBox"))
        self.label_7 = QtGui.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(7, 50, 16, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.unitsHeightComboBox = QtGui.QComboBox(self.frame_3)
        self.unitsHeightComboBox.setGeometry(QtCore.QRect(110, 50, 61, 26))
        self.unitsHeightComboBox.setObjectName(_fromUtf8("unitsHeightComboBox"))
        self.unitsHeightComboBox.addItem(_fromUtf8(""))
        self.unitsHeightComboBox.addItem(_fromUtf8(""))
        self.label_8 = QtGui.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(70, 0, 62, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(10, 10, 31, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.resourceLabel = QtGui.QLabel(self.frame)
        self.resourceLabel.setGeometry(QtCore.QRect(50, 10, 141, 16))
        self.resourceLabel.setText(_fromUtf8(""))
        self.resourceLabel.setObjectName(_fromUtf8("resourceLabel"))
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1096, 22))
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
        self.label.setText(_translate("MainWindow", "ID", None))
        self.unitsXComboBox.setItemText(0, _translate("MainWindow", "Px", None))
        self.unitsXComboBox.setItemText(1, _translate("MainWindow", "%", None))
        self.label_2.setText(_translate("MainWindow", "X", None))
        self.label_3.setText(_translate("MainWindow", "Y", None))
        self.unitsYComboBox.setItemText(0, _translate("MainWindow", "Px", None))
        self.unitsYComboBox.setItemText(1, _translate("MainWindow", "%", None))
        self.label_5.setText(_translate("MainWindow", "Position", None))
        self.horizontalAlignmentBox.setTitle(_translate("MainWindow", "Horizontal", None))
        self.alignLeftRadio.setText(_translate("MainWindow", "Left", None))
        self.alignRightRadio.setText(_translate("MainWindow", "Right", None))
        self.verticalAlignmentBox.setTitle(_translate("MainWindow", "Vertical", None))
        self.alignBottomRadio.setText(_translate("MainWindow", "Btm", None))
        self.alignTopRadio.setText(_translate("MainWindow", "Top", None))
        self.label_4.setText(_translate("MainWindow", "Align", None))
        self.unitsWidthComboBox.setItemText(0, _translate("MainWindow", "Px", None))
        self.unitsWidthComboBox.setItemText(1, _translate("MainWindow", "%", None))
        self.label_6.setText(_translate("MainWindow", "W", None))
        self.label_7.setText(_translate("MainWindow", "H", None))
        self.unitsHeightComboBox.setItemText(0, _translate("MainWindow", "Px", None))
        self.unitsHeightComboBox.setItemText(1, _translate("MainWindow", "%", None))
        self.label_8.setText(_translate("MainWindow", "Size", None))
        self.label_9.setText(_translate("MainWindow", "Res.", None))
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
