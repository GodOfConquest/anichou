# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created: Tue Sep 18 22:49:08 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AniChou(object):
    def setupUi(self, AniChou):
        AniChou.setObjectName(_fromUtf8("AniChou"))
        AniChou.resize(800, 600)
        self.centralwidget = QtGui.QWidget(AniChou)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tracker = QtGui.QLabel(self.centralwidget)
        self.tracker.setEnabled(True)
        self.tracker.setFrameShape(QtGui.QFrame.Panel)
        self.tracker.setFrameShadow(QtGui.QFrame.Sunken)
        self.tracker.setText(_fromUtf8(""))
        self.tracker.setObjectName(_fromUtf8("tracker"))
        self.verticalLayout.addWidget(self.tracker)
        self.statusTabs = QtGui.QTabWidget(self.centralwidget)
        self.statusTabs.setObjectName(_fromUtf8("statusTabs"))
        self.verticalLayout.addWidget(self.statusTabs)
        AniChou.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AniChou)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        AniChou.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AniChou)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AniChou.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(AniChou)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        AniChou.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionQuit = QtGui.QAction(AniChou)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionPlaybar = QtGui.QAction(AniChou)
        self.actionPlaybar.setCheckable(True)
        self.actionPlaybar.setChecked(False)
        self.actionPlaybar.setObjectName(_fromUtf8("actionPlaybar"))
        self.actionParameters = QtGui.QAction(AniChou)
        self.actionParameters.setObjectName(_fromUtf8("actionParameters"))
        self.actionAbout = QtGui.QAction(AniChou)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/data/acbt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionSync = QtGui.QAction(AniChou)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/data/sync.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSync.setIcon(icon1)
        self.actionSync.setObjectName(_fromUtf8("actionSync"))
        self.menuFile.addAction(self.actionSync)
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionPlaybar)
        self.menuEdit.addAction(self.actionParameters)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionSync)
        self.toolBar.addAction(self.actionAbout)

        self.retranslateUi(AniChou)
        self.statusTabs.setCurrentIndex(-1)
        QtCore.QObject.connect(self.actionPlaybar, QtCore.SIGNAL(_fromUtf8("triggered(bool)")), AniChou.toggleTracker)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("activated()")), AniChou.close)
        QtCore.QObject.connect(self.actionSync, QtCore.SIGNAL(_fromUtf8("activated()")), AniChou.sync)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL(_fromUtf8("activated()")), AniChou.showAboutDialog)
        QtCore.QObject.connect(self.actionParameters, QtCore.SIGNAL(_fromUtf8("activated()")), AniChou.showPreferencesDialog)
        QtCore.QMetaObject.connectSlotsByName(AniChou)

    def retranslateUi(self, AniChou):
        AniChou.setWindowTitle(QtGui.QApplication.translate("AniChou", "AniChou", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("AniChou", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("AniChou", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("AniChou", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("AniChou", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("AniChou", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("AniChou", "Alt+F4", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlaybar.setText(QtGui.QApplication.translate("AniChou", "Playbar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionParameters.setText(QtGui.QApplication.translate("AniChou", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("AniChou", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSync.setText(QtGui.QApplication.translate("AniChou", "S&ynchronize", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSync.setToolTip(QtGui.QApplication.translate("AniChou", "Synchronize", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSync.setShortcut(QtGui.QApplication.translate("AniChou", "Ctrl+Y", None, QtGui.QApplication.UnicodeUTF8))

import AniChou.gui.images_rc
