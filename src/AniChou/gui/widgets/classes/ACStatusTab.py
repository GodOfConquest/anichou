# -*- coding: utf-8 -*-

import logging

from PyQt4 import QtCore, QtGui
from AniChou import settings
from AniChou.db.data import LOCAL_TYPE
from AniChou.gui.widgets import (ACReadOnlyDelegate, ACSpinBoxDelegate,
        ACComboBoxDelegate, ACProgressBarDelegate, ACColorDelegate)


class ACStatusTab(QtGui.QTableView):

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

