# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from AniChou.db.data import LOCAL_TYPE
from AniChou.gui.widgets import ACSpinBoxDelegate, ACComboBoxDelegate

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

SCORE_VALUES = [str(i) for i in range(1, 11)]


def cell_factory(calculator, data, parent_class=QtGui.QTableWidgetItem):
    class ACTableCell(parent_class):
        _data = data

        def calculateCell(self):
            pass

        if calculator:
            calculateCell = calculator

        def __init__(self, parent=None, editable=False):
            if parent_class is QtGui.QTableWidgetItem:
                parent_class.__init__(self, 0)
                if editable:
                    flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
                else:
                    flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                self.setFlags(flags)
            else:
                parent_class.__init__(self, parent)
            self.calculateCell()

    return ACTableCell


class ACStatusTab(object):

    status = 0

    def __init__(self, parent=None):
        self._table = table = self.ui.tableWidget
        for size in COLUMN_SIZES:
            table.horizontalHeader().resizeSection(*size)
        headers = dict([(val, key) for key, val in COLUMN_HEADERS])
        self.my_score_delegate = ACComboBoxDelegate(self, SCORE_VALUES)
        self.episodes_delegate = ACSpinBoxDelegate(self)
        table.setItemDelegateForColumn(headers['my_score'], self.my_score_delegate)
        table.setItemDelegateForColumn(headers['episodes'], self.episodes_delegate)

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
            if isinstance(cell, QtGui.QTableWidgetItem):
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
        def calc(self):
            self.setText(unicode(getattr(anime, cellname)))
        return cell_factory(calc, anime)()

    def cell_changed(self, anime):
        def calc(self):
            if not self._data._changed:
                color = QtGui.QColor(100, 180, 0)
            else:
                color = QtGui.QColor(255, 50, 50)
            self.setBackgroundColor(color)
        return cell_factory(calc, anime)()

    def cell_type(self, anime):
        def calc(self):
            self.setText(unicode(dict(LOCAL_TYPE)[self._data.type]))
        return cell_factory(calc, anime)()

    def cell_my_score(self, anime):
        return cell_factory(lambda self: \
            self.setText(unicode(self._data.my_score)), anime)(editable=True)

    def cell_episodes(self, anime):
        # Extract episodes/max and construct display string
        def calc(self):
            anime = self._data
            episodes = [unicode(anime.my_episodes)]
            if anime.episodes:
                episodes.append(unicode(anime.episodes))
            self.setText('/'.join(episodes))
        return cell_factory(calc, anime)(editable=True)

    def cell_progress(self, anime):
        # Calculate progress bar
        def calc(self):
            try:
                progress = int(float(self._data.my_episodes) / float(self._data.episodes) * 100)
            except:
                progress = 0
            self.setValue(progress)
        pbar = cell_factory(calc, anime, QtGui.QProgressBar)()
        pbar.setRange(0, 100)
        return pbar
