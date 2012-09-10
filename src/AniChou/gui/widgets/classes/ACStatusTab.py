# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


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
        for key, anime in data.items():
            # Extract series title
            name = anime['title']
            name = name.replace('&apos;', '\'')

            # Extract episodes/max and construct display string
            if anime['episodes']:
                max_episodes = anime['episodes']
            else:
                max_episodes = '-'
            current_episode = anime['status_episodes']
            episodes = (current_episode, max_episodes)

            # Calculate progress bar
            progress = 0
            try:
                progress = int(float(current_episode) / float(max_episodes) * 100)
            except:
                progress = 0

            # Extract score
            score = anime['status_score']

            # Construct row list and add it to the liststore
            row = [name, anime['type'], anime['sources'], score,
                    episodes, progress]

            # Store key in row position
            self.keylist.append(key)

    def addRow(self, data):
        if len(data) < 6:
            raise ValueError('It must be at least 6 elements to fill row')
        table = self._table
        row = table.rowCount()
        table.insertRow(row)

        # Title, sources, type
        for col in range(0, 3):
            table.setItem(col, row, QtGui.QTableWidgetItem(data[col]))

        # Rating
        table.setItem(3, row, QtGui.QTableWidgetItem(data[3]))

        # Episodes
        table.setItem(4, row, QtGui.QTableWidgetItem('/'.join(data[4])))

        #Progress
        progress = QtGui.QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(data[5])
        table.setCellWidget(4, row, progress)

