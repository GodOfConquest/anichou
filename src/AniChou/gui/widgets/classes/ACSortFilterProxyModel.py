# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from AniChou import settings


class ACSortFilterProxyModel(QtGui.QSortFilterProxyModel):

    def __init__(self, parent=None, model=None, stindex=None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        if model:
            self.setSourceModel(model)
        if stindex is not None:
            self.style = settings.GUI_COLUMNS.get_by_index(stindex)

    def headerData(self, section, orientation, role):
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return QtGui.QSortFilterProxyModel.headerData(self, section, orientation, role)
        try:
            data = dict(self.style['title'])[section]
        except KeyError:
            data = unicode(section)
        return data

    def columnName(self, index):
        column = index.column()
        return dict(self.style['name'])[column]

    def data(self, index, role):
        return self.sourceModel().data(self.mapToSource(index),
                                        role, self.columnName(index))

    def setData(self, index, value, role):
        self.sourceModel().setData(self.mapToSource(index),
                                value, role, self.columnName(index))
