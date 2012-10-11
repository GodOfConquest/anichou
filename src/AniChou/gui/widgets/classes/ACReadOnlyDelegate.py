# -*- coding: utf-8 -*

from PyQt4 import QtGui


class ACReadOnlyDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        return None
