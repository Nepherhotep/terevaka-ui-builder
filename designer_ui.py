# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer.ui'
#
# Created: Mon Apr 22 18:48:45 2013
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
        MainWindow.resize(1106, 557)
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
        self.sprites.setGeometry(QtCore.QRect(0, 0, 200, 420))
        self.sprites.setObjectName(_fromUtf8("sprites"))
        self.spritesListWidget = QtGui.QListWidget(self.sprites)
        self.spritesListWidget.setGeometry(QtCore.QRect(10, 0, 181, 421))
        self.spritesListWidget.setViewMode(QtGui.QListView.IconMode)
        self.spritesListWidget.setObjectName(_fromUtf8("spritesListWidget"))
        self.toolBox.addItem(self.sprites, _fromUtf8(""))
        self.properties = QtGui.QWidget()
        self.properties.setGeometry(QtCore.QRect(0, 0, 200, 420))
        self.properties.setObjectName(_fromUtf8("properties"))
        self.groupBox = QtGui.QGroupBox(self.properties)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 181, 51))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.workingDirLabel = QtGui.QLabel(self.groupBox)
        self.workingDirLabel.setGeometry(QtCore.QRect(11, 20, 131, 31))
        self.workingDirLabel.setObjectName(_fromUtf8("workingDirLabel"))
        self.workingDirToolButton = QtGui.QToolButton(self.groupBox)
        self.workingDirToolButton.setGeometry(QtCore.QRect(146, 24, 27, 20))
        self.workingDirToolButton.setObjectName(_fromUtf8("workingDirToolButton"))
        self.groupBox_2 = QtGui.QGroupBox(self.properties)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 50, 181, 51))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.layoutPathLabel = QtGui.QLabel(self.groupBox_2)
        self.layoutPathLabel.setGeometry(QtCore.QRect(11, 20, 131, 31))
        self.layoutPathLabel.setObjectName(_fromUtf8("layoutPathLabel"))
        self.layoutPathToolButton = QtGui.QToolButton(self.groupBox_2)
        self.layoutPathToolButton.setGeometry(QtCore.QRect(146, 24, 27, 20))
        self.layoutPathToolButton.setObjectName(_fromUtf8("layoutPathToolButton"))
        self.layoutSizeLabel = QtGui.QLabel(self.properties)
        self.layoutSizeLabel.setEnabled(False)
        self.layoutSizeLabel.setGeometry(QtCore.QRect(65, 110, 91, 20))
        self.layoutSizeLabel.setObjectName(_fromUtf8("layoutSizeLabel"))
        self.layoutWidthSpinBox = QtGui.QDoubleSpinBox(self.properties)
        self.layoutWidthSpinBox.setEnabled(False)
        self.layoutWidthSpinBox.setGeometry(QtCore.QRect(37, 128, 111, 25))
        self.layoutWidthSpinBox.setToolTip(_fromUtf8(""))
        self.layoutWidthSpinBox.setDecimals(2)
        self.layoutWidthSpinBox.setMaximum(99999.0)
        self.layoutWidthSpinBox.setProperty("value", 853.0)
        self.layoutWidthSpinBox.setObjectName(_fromUtf8("layoutWidthSpinBox"))
        self.layoutHeightLabel = QtGui.QLabel(self.properties)
        self.layoutHeightLabel.setEnabled(False)
        self.layoutHeightLabel.setGeometry(QtCore.QRect(20, 160, 16, 21))
        self.layoutHeightLabel.setObjectName(_fromUtf8("layoutHeightLabel"))
        self.anchorXLabel_4 = QtGui.QLabel(self.properties)
        self.anchorXLabel_4.setEnabled(False)
        self.anchorXLabel_4.setGeometry(QtCore.QRect(155, 132, 16, 21))
        self.anchorXLabel_4.setObjectName(_fromUtf8("anchorXLabel_4"))
        self.layoutHeightSpinBox = QtGui.QDoubleSpinBox(self.properties)
        self.layoutHeightSpinBox.setEnabled(False)
        self.layoutHeightSpinBox.setGeometry(QtCore.QRect(37, 158, 111, 25))
        self.layoutHeightSpinBox.setDecimals(2)
        self.layoutHeightSpinBox.setMaximum(99999.99)
        self.layoutHeightSpinBox.setProperty("value", 640.0)
        self.layoutHeightSpinBox.setObjectName(_fromUtf8("layoutHeightSpinBox"))
        self.layoutWidthLabel = QtGui.QLabel(self.properties)
        self.layoutWidthLabel.setEnabled(False)
        self.layoutWidthLabel.setGeometry(QtCore.QRect(20, 130, 16, 21))
        self.layoutWidthLabel.setObjectName(_fromUtf8("layoutWidthLabel"))
        self.anchorXLabel_5 = QtGui.QLabel(self.properties)
        self.anchorXLabel_5.setEnabled(False)
        self.anchorXLabel_5.setGeometry(QtCore.QRect(155, 162, 16, 21))
        self.anchorXLabel_5.setObjectName(_fromUtf8("anchorXLabel_5"))
        self.toolBox.addItem(self.properties, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.toolBox)
        self.graphicsViewContainer = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsViewContainer.sizePolicy().hasHeightForWidth())
        self.graphicsViewContainer.setSizePolicy(sizePolicy)
        self.graphicsViewContainer.setObjectName(_fromUtf8("graphicsViewContainer"))
        self.graphicsView = DesignerGraphicsView(self.graphicsViewContainer)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 641, 481))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsViewContainer)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(200, 0))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.resourceIdEdit = QtGui.QLineEdit(self.frame)
        self.resourceIdEdit.setGeometry(QtCore.QRect(40, 40, 151, 22))
        self.resourceIdEdit.setInputMask(_fromUtf8(""))
        self.resourceIdEdit.setText(_fromUtf8(""))
        self.resourceIdEdit.setPlaceholderText(_fromUtf8(""))
        self.resourceIdEdit.setObjectName(_fromUtf8("resourceIdEdit"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(7, 41, 31, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 80, 181, 221))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.posXSpinBox = QtGui.QDoubleSpinBox(self.frame_2)
        self.posXSpinBox.setGeometry(QtCore.QRect(20, 20, 151, 25))
        self.posXSpinBox.setDecimals(2)
        self.posXSpinBox.setMaximum(99999.0)
        self.posXSpinBox.setObjectName(_fromUtf8("posXSpinBox"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(7, 22, 16, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.posYSpinBox = QtGui.QDoubleSpinBox(self.frame_2)
        self.posYSpinBox.setGeometry(QtCore.QRect(20, 50, 151, 25))
        self.posYSpinBox.setDecimals(2)
        self.posYSpinBox.setMaximum(99999.99)
        self.posYSpinBox.setObjectName(_fromUtf8("posYSpinBox"))
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(7, 52, 16, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_5 = QtGui.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(21, 0, 141, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalAlignmentBox = QtGui.QGroupBox(self.frame_2)
        self.horizontalAlignmentBox.setGeometry(QtCore.QRect(10, 90, 161, 111))
        self.horizontalAlignmentBox.setObjectName(_fromUtf8("horizontalAlignmentBox"))
        self.alignLeftRadio = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignLeftRadio.setGeometry(QtCore.QRect(10, 30, 61, 20))
        self.alignLeftRadio.setChecked(False)
        self.alignLeftRadio.setObjectName(_fromUtf8("alignLeftRadio"))
        self.alignRightRadio = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignRightRadio.setGeometry(QtCore.QRect(10, 70, 61, 20))
        self.alignRightRadio.setObjectName(_fromUtf8("alignRightRadio"))
        self.alignCenterRadio = QtGui.QRadioButton(self.horizontalAlignmentBox)
        self.alignCenterRadio.setGeometry(QtCore.QRect(10, 50, 102, 20))
        self.alignCenterRadio.setChecked(True)
        self.alignCenterRadio.setObjectName(_fromUtf8("alignCenterRadio"))
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(10, 10, 31, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.resourceLabel = QtGui.QLabel(self.frame)
        self.resourceLabel.setGeometry(QtCore.QRect(50, 10, 141, 16))
        self.resourceLabel.setText(_fromUtf8(""))
        self.resourceLabel.setObjectName(_fromUtf8("resourceLabel"))
        self.dropPanel = DropPanel(self.frame)
        self.dropPanel.setGeometry(QtCore.QRect(10, 310, 181, 71))
        self.dropPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.dropPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.dropPanel.setObjectName(_fromUtf8("dropPanel"))
        self.label_10 = QtGui.QLabel(self.dropPanel)
        self.label_10.setGeometry(QtCore.QRect(10, 25, 161, 21))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1106, 22))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuResources = QtGui.QMenu(self.menubar)
        self.menuResources.setEnabled(True)
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
        self.actionSet_Layout_Path = QtGui.QAction(MainWindow)
        self.actionSet_Layout_Path.setObjectName(_fromUtf8("actionSet_Layout_Path"))
        self.actionExport_Layout = QtGui.QAction(MainWindow)
        self.actionExport_Layout.setObjectName(_fromUtf8("actionExport_Layout"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuResources.addAction(self.actionSet_Dir)
        self.menuResources.addAction(self.actionSet_Layout_Path)
        self.menuResources.addAction(self.actionExport_Layout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuResources.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.sprites), _translate("MainWindow", "Sprites", None))
        self.groupBox.setTitle(_translate("MainWindow", "Working dir", None))
        self.workingDirLabel.setText(_translate("MainWindow", "Not Specified", None))
        self.workingDirToolButton.setText(_translate("MainWindow", "...", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Layout path", None))
        self.layoutPathLabel.setText(_translate("MainWindow", "Not Specified", None))
        self.layoutPathToolButton.setText(_translate("MainWindow", "...", None))
        self.layoutSizeLabel.setText(_translate("MainWindow", "Layout Size", None))
        self.layoutHeightLabel.setText(_translate("MainWindow", "H", None))
        self.anchorXLabel_4.setText(_translate("MainWindow", "Px", None))
        self.layoutWidthLabel.setText(_translate("MainWindow", "W", None))
        self.anchorXLabel_5.setText(_translate("MainWindow", "Px", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.properties), _translate("MainWindow", "Properties", None))
        self.label.setText(_translate("MainWindow", "UID", None))
        self.label_2.setText(_translate("MainWindow", "X", None))
        self.label_3.setText(_translate("MainWindow", "Y", None))
        self.label_5.setText(_translate("MainWindow", "Position", None))
        self.horizontalAlignmentBox.setTitle(_translate("MainWindow", "Horizontal Align", None))
        self.alignLeftRadio.setText(_translate("MainWindow", "Left", None))
        self.alignRightRadio.setText(_translate("MainWindow", "Right", None))
        self.alignCenterRadio.setText(_translate("MainWindow", "Center", None))
        self.label_9.setText(_translate("MainWindow", "Res.", None))
        self.label_10.setText(_translate("MainWindow", "Drag here to Drop", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuResources.setTitle(_translate("MainWindow", "Resources", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionUndo.setText(_translate("MainWindow", "Undo", None))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z", None))
        self.actionSet_Dir.setText(_translate("MainWindow", "Set Dir", None))
        self.actionSet_Dir.setShortcut(_translate("MainWindow", "Ctrl+D", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionRedo.setText(_translate("MainWindow", "Redo", None))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y", None))
        self.actionSet_Layout_Path.setText(_translate("MainWindow", "Set Layout Path", None))
        self.actionSet_Layout_Path.setShortcut(_translate("MainWindow", "Ctrl+L", None))
        self.actionExport_Layout.setText(_translate("MainWindow", "Export Layout", None))
        self.actionExport_Layout.setShortcut(_translate("MainWindow", "Ctrl+Return", None))
        self.actionSave_As.setText(_translate("MainWindow", "Save As ...", None))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S", None))

from graphicsview import DesignerGraphicsView
from drop_panel import DropPanel
