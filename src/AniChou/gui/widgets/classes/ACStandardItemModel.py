# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from AniChou import settings
from AniChou.db.data import LOCAL_TYPE


LOCAL_TYPE_DICT = dict(LOCAL_TYPE)
COLUMN_NAMES = dict(settings.GUI_COLUMNS['name'])
SCORE_VALUES = [str(i) for i in range(1, 11)]

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

        name = COLUMN_NAMES[index.column()]
        if role == Qt.DisplayRole:
            try:
                cell = getattr(self, 'cell_' + name)(item.dbmodel)
            except AttributeError:
                cell = self.cell_default(name, item.dbmodel)
            return cell
        elif role == Qt.EditRole:
            try:
                cell = getattr(self, 'get_cell_' + name)(item.dbmodel)
            except AttributeError:
                pass
            else:
                return cell
        elif role == Qt.DecorationRole:
            try:
                cell = getattr(self, 'decorate_cell_' + name)(item.dbmodel)
            except AttributeError:
                pass
            else:
                return cell

        return QtGui.QStandardItemModel.data(self, index, role)

    def setData(self, index, value, role):
        item = self.itemFromIndex(index.sibling(index.row(), 0))
        if type(item) == QtGui.QStandardItem:
            QtGui.QStandardItemModel.setData(self, index, value, role)
            return

        name = COLUMN_NAMES[index.column()]
        if role == Qt.EditRole:
            try:
                getattr(self, 'set_cell_' + name)(item.dbmodel, value)
                return
            except AttributeError:
                pass

        QtGui.QStandardItemModel.setData(self, index, value, role)


    def cell_default(self, cellname, anime):
        return unicode(getattr(anime, cellname))

    def cell_changed(self, anime):
        return ''

    def decorate_cell_changed(self, anime):
        if anime._changed:
            return (255, 50, 50)
        return (100, 180, 0)

    def cell_type(self, anime):
        return unicode(LOCAL_TYPE_DICT[anime.type])

    def cell_episodes(self, anime):
        # Extract episodes/max and construct display string
        episodes = []
        if anime.my_episodes:
            episodes.append(unicode(anime.my_episodes))
        episodes.append(unicode(anime.episodes or '~'))
        return '/'.join(episodes)

    def get_cell_episodes(self, anime):
        return anime.my_episodes

    def set_cell_episodes(self, anime, value):
        anime.my_episodes = value

    def decorate_cell_episodes(self, anime):
        return (0, anime.episodes)

    def get_cell_my_score(self, anime):
        return anime.my_score

    def set_cell_my_score(self, anime, value):
        try:
            index = SCORE_VALUES.index(value)
            anime.my_score = index + 1
        except IndexError:
            anime.my_score = 0


    def decorate_cell_my_score(self, anime):
        return SCORE_VALUES

    def cell_progress(self, anime):
        try:
            progress = int(float(anime.my_episodes) / float(anime.episodes) * 100)
        except:
            progress = 0
        return progress
