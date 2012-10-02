# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from AniChou.db.models import LOCAL_TYPE


class ACStatusTab(object):

    status = 0

    def __init__(self, parent=None):
        self.keylist = []
        self._table = self.ui.tableWidget

    def clear(self):
        """ Removes all rows from table """
        self.keylist[:] = []
        while self._table.rowCount():
            self._table.removeRow(1)

    def updateData(self, data):
        """
        Clear table and add new data.
        """
        self.clear()
        for anime in data:
            name = anime.title

            # Extract episodes/max and construct display string
            if anime.episodes:
                max_episodes = anime.episodes
            else:
                max_episodes = '-'
            current_episode = anime.my_episodes
            episodes = (current_episode, max_episodes)

            # Construct row list and add it to the liststore
            row = [anime.title, dict(LOCAL_TYPE)[anime.type],
                   anime.sources, anime.my_score, episodes]
            self.addRow(row)

            # Store key in row position
            self.keylist.append(anime)

    def addRow(self, data):
        if len(data) < 5:
            raise ValueError('It must be at least 6 elements to fill row')
        table = self._table
        row = table.rowCount()
        table.insertRow(row)

        # Title, sources, type
        for col in range(0, 3):
            table.setItem(row, col, QtGui.QTableWidgetItem(unicode(data[col])))

        # Rating
        table.setItem(row, 3, QtGui.QTableWidgetItem(data[3]))

        # Episodes
        episodes = data[4]
        table.setItem(row, 4, QtGui.QTableWidgetItem(
                '/'.join([unicode(f) for f in episodes])))

        #Progress
        # Calculate progress bar
        try:
            progress = int(float(episodes[0]) / float(episodes[1]) * 100)
        except:
            progress = 0
        pbar = QtGui.QProgressBar()
        pbar.setRange(0, 100)
        pbar.setValue(progress)
        table.setCellWidget(row, 5, pbar)

