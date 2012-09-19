
import os

from PyQt4 import QtCore, QtGui
from AniChou.config import BaseConfig


class ACDirectoryListWidget(QtGui.QListWidget):

    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.cfg = getattr(self.window(), 'cfg', BaseConfig())

    def listContextMenu(self, pos):
        menu = QtGui.QMenu()
        item = self.itemAt(pos)
        #This shit sends without event
        a = menu.addAction("Add item")
        #oh, lol
        self.connect(a, QtCore.SIGNAL('triggered()'),
                        lambda r=item: self.chooseItem(r))
        menu.addAction(a)
        if item:
            d = menu.addAction("Delete item")
            self.connect(d, QtCore.SIGNAL('triggered()'),
                        lambda r=item: self.removeItem(r))
            menu.addAction(d)
        menu.exec_(self.mapToGlobal(pos))

    def removeItem(self, item):
        #lol
        self.takeItem(self.row(item))

    def removeCurrent(self):
        self.removeItem(self.currentItem())

    def chooseItem(self, aitem=None):
        name = QtGui.QFileDialog.getExistingDirectory(self,
                'Add tracking folder', self.cfg.startup.get('last_dir') or '.',
                QtGui.QFileDialog.ShowDirsOnly)
        if not name:
            return
        self.cfg.startup['last_dir'] = os.path.abspath(os.path.join(
                                                str(name), os.pardir))
        item = QtGui.QListWidgetItem(name)
        row = self.row(aitem)
        if row < 0:
            self.addItem(item)
        else:
            self.insertItem(row, item)
        self._changed()

    def getValue(self):
        data = []
        for i in range(self.count()):
            data.append(str(self.item(i).text()))
        return data

    def setValue(self, data):
        self.clear()
        if type(data) in (list, tuple):
            for name in data:
                self.addItem(QtGui.QListWidgetItem(name))
        self._changed(data)

    def _changed(self, *data):
        types = ', '.join(map(lambda x: type(x).__name__, data))
        self.emit(QtCore.SIGNAL("valueChanged(%s)" % types), *data)
