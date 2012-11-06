# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from AniChou import settings
from AniChou.db.data import LOCAL_TYPE, LOCAL_STATUS_R
from AniChou.services import ServiceManager
from AniChou.utils import DefaultDict


LOCAL_TYPE_DICT = dict(LOCAL_TYPE)
SCORE_VALUES = [unicode(i) for i in range(1, 11)]
COLUMN_NAMES = DefaultDict([
    (v, dict(settings.GUI_COLUMNS[v]['name'])) \
        for v in settings.GUI_COLUMNS['index'].values()
])
COLUMN_NAMES['index'] = settings.GUI_COLUMNS['index']


class ACStandardItemModel(QtGui.QStandardItemModel):
    ACTIONS = dict((
        (Qt.DisplayRole, 'cell_'),
        (Qt.EditRole, 'get_cell_'),
        (Qt.DecorationRole, 'decorate_cell_'),
    ))

    def __init__(self, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        columns = max([len(v.get('name', [])) \
             for k, v in settings.GUI_COLUMNS.items() \
                if k != 'index'])
        self.setColumnCount(columns)
        #self.setHorizontalHeaderLabels([i for v, i in columns])

    def columnName(self, column):
        #return COLUMN_NAMES.get_by_index(item.parent().text())[column]
        return dict(settings.GUI_COLUMNS['default']['name'])[column]

    def data(self, index, role, name=None):
        item = self.itemFromIndex(index.sibling(index.row(), 0))
        column = index.column()
        if role not in self.ACTIONS.keys() or \
                type(item) == QtGui.QStandardItem or column < 0:
            return QtGui.QStandardItemModel.data(self, index, role)
        if name is None:
            name = self.columnName(column)
        if role == Qt.DisplayRole:
            try:
                cell = getattr(self, self.ACTIONS[role] + name)(item.dbmodel)
            except AttributeError, e:
                cell = self.cell_default(name, item.dbmodel)
            return cell
        else:
            try:
                cell = getattr(self, self.ACTIONS[role] + name)(item.dbmodel)
            except AttributeError:
                pass
            else:
                return cell

        return QtGui.QStandardItemModel.data(self, index, role)

    def setData(self, index, value, role, name=None):
        item = self.itemFromIndex(index.sibling(index.row(), 0))
        if type(item) == QtGui.QStandardItem:
            QtGui.QStandardItemModel.setData(self, index, value, role)
            return
        if name is None:
            name = self.columnName(column)
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
        if anime._changed > ServiceManager.last_sync:
            return (255, 50, 50)
        return (100, 180, 0)

    def cell_type(self, anime):
        return unicode(LOCAL_TYPE_DICT[anime.type])

    def cell_sources(self, anime):
        return anime.sources

    def cell_episodes(self, anime):
        # Extract episodes/max and construct display string
        episodes = []
        if anime.my_status in (LOCAL_STATUS_R['watching'],
                               LOCAL_STATUS_R['dropped'],
                               LOCAL_STATUS_R['hold']):
            episodes.append(unicode(anime.my_episodes or 0))
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
