# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from AniChou import settings
from AniChou.db.data import LOCAL_TYPE


LOCAL_TYPE_DICT = dict(LOCAL_TYPE)


class ACStandardItemModel(QtGui.QStandardItemModel):

    def __init__(self, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        columns = settings.GUI_COLUMNS['title']
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels([i for v, i in columns])

    def data(self, index, role):
        item = self.itemFromIndex(index.sibling(index.row(), 0))
        if type(item) == QtGui.QStandardItem:
            return QtGui.QStandardItemModel.data(self, index, role)


        if role == Qt.DisplayRole:
            name = settings.GUI_COLUMNS['name'][index.column()][-1]
            try:
                cell = getattr(self, 'cell_' + name)(item.dbmodel)
            except AttributeError:
                cell = self.cell_default(name, item.dbmodel)
            return cell

        return QtGui.QStandardItemModel.data(self, index, role)


    def cell_default(self, cellname, anime):
        return unicode(getattr(anime, cellname))

    def cell_changed(self, anime):
        return ''

    def cell_type(self, anime):
        return unicode(LOCAL_TYPE_DICT[anime.type])

    def cell_episodes(self, anime):
        # Extract episodes/max and construct display string
        episodes = []
        if anime.my_episodes:
            episodes.append(unicode(anime.my_episodes))
        episodes.append(unicode(anime.episodes or '~'))
        return '/'.join(episodes)

    def cell_progress(self, anime):
        try:
            progress = int(float(self._data.my_episodes) / float(self._data.episodes) * 100)
        except:
            progress = 0
        return progress
