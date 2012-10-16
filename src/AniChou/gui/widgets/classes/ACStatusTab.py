# -*- coding: utf-8 -*-

import logging
from PyQt4 import QtCore, QtGui
from AniChou import settings
from AniChou.db.data import LOCAL_STATUS
from AniChou.gui.widgets import (ACReadOnlyDelegate, ACSpinBoxDelegate,
        ACComboBoxDelegate, ACProgressBarDelegate, ACColorDelegate)



class ACStatusTab(QtGui.QTableView):

    status = 0

    def __init__(self, parent=None, model=None, index=None):
        QtGui.QTableView.__init__(self, parent)
        if model:
            self.setModel(model)
            if index:
                self.setRootIndex(index)

        # Styles
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        # self.setSortingEnabled(True)
        self.verticalHeader().hide()
        hheader = self.horizontalHeader()
        hheader.setStretchLastSection(True)
        hheader.setMinimumSectionSize(5)
        hheader.setHighlightSections(False)
        for size in settings.GUI_COLUMNS['size']:
            hheader.resizeSection(*size)

        controls = dict(settings.GUI_COLUMNS['controls'])
        # Controls
        rodelegate = ACReadOnlyDelegate(self)
        for number in range(0, model.columnCount()):
            if number not in controls.keys():
                self.setItemDelegateForColumn(number, rodelegate)
        for number, name in controls.items():
            try:
                delegate = globals()['AC{0}Delegate'.format(name)](self)
            except Exception as e:
                print e
                logging.error('Bad control {1} for column {0}'.format(number, name))
            else:
                self.setItemDelegateForColumn(number, delegate)

        # Context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuShow)

    def contextMenuShow(self, pos):
        menu = QtGui.QMenu()
        # Show item tabs
        parent = self.parent()
        # Parent is QStackedWidget here, so check where is QTabWidget
        while parent and not isinstance(parent, QtGui.QTabWidget):
            parent = parent.parent()
        if parent:
            tabs_menu = parent.contextMenuTabs(menu)
            menu.addMenu(tabs_menu)
        #Change item status
        row = self.rowAt(pos.y())
        if row >= 0:
            stat_menu = QtGui.QMenu(menu)
            stat_menu.setTitle("Set status")
            menu.addMenu(stat_menu)
            for number, title in LOCAL_STATUS:
                if number == self.status:
                    continue
                action = stat_menu.addAction(title)
                self.connect(action, QtCore.SIGNAL('triggered()'),
                        lambda r=row, s=number: self.changeStatus(r, s))
                #stat_menu.addAction(action)
        menu.exec_(self.mapToGlobal(pos))

    def changeStatus(self, row, status):
        """Changes status of item and moves it to another column"""
        model = self.model()
        try:
            parent = model.findItems(QtCore.QString(status))[0]
        except Exception as e:
            logging.error('changeStatus signal caused error:\n{0}'.format(e))
            return
        if not parent:
            logging.error('changeStatus status {0} not found.'.format(status))
            return
        root = model.itemFromIndex(self.rootIndex())
        row = root.takeRow(row)
        row[0].dbmodel.my_status = status
        parent.appendRow(row)
