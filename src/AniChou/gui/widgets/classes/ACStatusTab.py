# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from AniChou.db.data import LOCAL_TYPE


class ACStatusTab(object):

    status = 0

    def __init__(self, parent=None):
        self._table = self.ui.tableWidget

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

        for col, name in (  (0, 'title'),
                            (1, 'type'),
                            (2, 'sources'),
                            (3, 'my_score'),
                            (4, 'episodes'),
                            (5, 'progress')):
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
        return QtGui.QTableWidgetItem(unicode(getattr(anime, cellname)))

    def cell_type(self, anime):
        return QtGui.QTableWidgetItem(unicode(dict(LOCAL_TYPE)[anime.type]))

    def cell_my_score(self, anime):
        return QtGui.QTableWidgetItem(anime.my_score)

    def cell_episodes(self, anime):
        # Extract episodes/max and construct display string
        episodes = [unicode(anime.my_episodes)]
        if anime.episodes:
            episodes.push(unicode(anime.episodes))
        return QtGui.QTableWidgetItem('/'.join(episodes))

    def cell_progress(self, anime):
                #Progress
        # Calculate progress bar
        try:
            progress = int(float(anime.my_episodes) / float(anime.episodes) * 100)
        except:
            progress = 0
        pbar = QtGui.QProgressBar()
        pbar.setRange(0, 100)
        pbar.setValue(progress)
        return pbar
