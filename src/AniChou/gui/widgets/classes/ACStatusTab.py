# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from AniChou.db.data import LOCAL_TYPE
from AniChou.gui.widgets import ACSpinBoxDelegate

COLUMN_HEADERS = (
    (0, 'changed'),
    (1, 'title'),
    (2, 'type'),
    (3, 'sources'),
    (4, 'my_score'),
    (5, 'episodes'),
    (6, 'progress')
)

COLUMN_SIZES = (
    (0, 7), (1, 300), (2, 50), (3, 60), (4, 50), (5, 70)
)




class ACStatusTab(object):

    status = 0

    def __init__(self, parent=None):
        self._table = table = self.ui.tableWidget
        for size in COLUMN_SIZES:
            table.horizontalHeader().resizeSection(*size)
        headers = dict([(val, key) for key, val in COLUMN_HEADERS])
        table.setItemDelegateForColumn(headers['my_score'], ACSpinBoxDelegate(self))

    def clear(self):
        """ Removes all rows from table """
        while self._table.rowCount():
            self._table.removeRow(0)

    def updateData(self, data):
        """
        Clear table and add new data.
        """
        if not data:
            return
        self.clear()
        for anime in data:
            self.addRow(anime)
        self._table.rowCount()

    def addRow(self, data):
        """
        Add new row to table.
        """
        table = self._table
        row = table.rowCount()
        table.insertRow(row)

        for col, name in COLUMN_HEADERS:
            try:
                cell = getattr(self, 'cell_' + name)(data)
            except AttributeError:
                cell = self.cell_default(name, data)
            cell._data = data
            if type(cell) == QtGui.QTableWidgetItem:
                table.setItem(row, col, cell)
            else:
                table.setCellWidget(row, col, cell)

    def getCellData(self, row, col):
        """
        Return data associated with cell.
        """
        table = self._table
        holder = table.item(row, col) or table.cellWidget(row, col)
        if holder:
            return holder._data
        return None

    # Cells for row
    def cell_default(self, cellname, anime):
        item = QtGui.QTableWidgetItem(unicode(getattr(anime, cellname)))
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        return item

    def cell_changed(self, anime):
        item = QtGui.QTableWidgetItem()
        def setChanged():
            if not anime._changed:
                color = QtGui.QColor(100, 180, 0)
            else:
                color = QtGui.QColor(255, 50, 50)
            item.setBackgroundColor(color)
        item.update_cell = setChanged
        item.update_cell()
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        return item

    def cell_type(self, anime):
        item = QtGui.QTableWidgetItem(unicode(dict(LOCAL_TYPE)[anime.type]))
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        return item

    def cell_my_score(self, anime):
        item = QtGui.QTableWidgetItem(anime.my_score)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        return item

    def cell_episodes(self, anime):
        # Extract episodes/max and construct display string
        episodes = [unicode(anime.my_episodes)]
        if anime.episodes:
            episodes.push(unicode(anime.episodes))
        return QtGui.QTableWidgetItem('/'.join(episodes))

    def cell_progress(self, anime):
        # Calculate progress bar
        pbar = QtGui.QProgressBar()
        pbar.setRange(0, 100)
        def calculate():
            try:
                progress = int(float(anime.my_episodes) / float(anime.episodes) * 100)
            except:
                progress = 0
            pbar.setValue(progress)
        pbar.calculate_cell = calculate
        pbar.calculate_cell()
        return pbar
