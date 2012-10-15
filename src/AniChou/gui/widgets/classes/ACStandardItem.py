# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class ACStandardItem(QtGui.QStandardItem):
    def __init__(self, label, data):
        QtGui.QStandardItem.__init__(self, label)
        self.dbmodel = data
