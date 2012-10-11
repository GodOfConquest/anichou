
import logging
import time

from PyQt4 import QtCore, QtGui
from AniChou import players, recognizinig
from AniChou import settings
from AniChou import signals
from AniChou.db.models import Anime
from AniChou.gui.Main import Ui_AniChou
from AniChou.gui.widgets import ( ACStatusTab, ACAboutDialog,
            ACPreferencesDialog, ACStandardItemModel, ACStandardItem )
from AniChou.services.data.base import LOCAL_STATUS


__all__ = ['get_app', 'Main']


def get_app(argv):
    return QtGui.QApplication(argv)


class Main(QtGui.QMainWindow):

    def __init__(self, manager, cfg):
        self.manager = manager
        self.cfg = cfg
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_AniChou()
        self.ui.setupUi(self)
        self.createTabs()

        # GUI backend must process application-level signals if it has
        # its own main loop
        self.supportTimer = QtCore.QTimer(self)

        # Sync on start
        if self.cfg.startup.get('sync'):
            QtCore.QTimer.singleShot(100, self, QtCore.SLOT('sync()'))

        # Register signals
        signals.Slot('notify', self.notify)
        signals.Slot('gui_tables_update', self.updateFromDB)
        signals.Slot('set_track_message', self.setTrackMessage)

        # Setup tracker
        self.tracker = signals.Signal()
        self.tracker.connect('start_tracker')
        self.tracker.connect('stop_tracker')
        self.toggleTracker(cfg.startup.get('tracker'))
        self.updateFromDB()
        self.connect(self.supportTimer, QtCore.SIGNAL('timeout()'), self.supportThread);
        self.supportTimer.start(0.01)

    def createTabs(self):
        # Create tabs
        stabs = self.ui.statusTabs
        self.model = model = ACStandardItemModel()
        parentItem = self.model.invisibleRootItem()
        columns = len(settings.GUI_COLUMNS['name']) - 1
        for number, title in LOCAL_STATUS:
            # Add model group
            item = QtGui.QStandardItem(QtCore.QString(number))
            parentItem.appendRow(item)
            item.insertColumns(1, columns)
            # Do not create tab for None status
            if not number:
                continue

            # Create tab and set its model
            index = self.model.index(model.rowCount() - 1, 0)
            tab = ACStatusTab(stabs, model, index);
            tab.status = number
            stabs.addTab(tab, title)


    def supportThread(self):
        """
        This function processes application-level signals.
        """
        signals.process()

    #@signals.Slot('notify')
    def notify(self, message):
        self.ui.statusbar.showMessage(message)

    @QtCore.pyqtSlot()
    def clearMessage(self):
        self.ui.statusbar.clearMessage()

    @QtCore.pyqtSlot(bool)
    def toggleTracker(self, value):
        value = bool(value)
        if value:
            signals.emit(self.tracker, 'start_tracker')
        else:
            signals.emit(self.tracker, 'stop_tracker')
        self.ui.actionPlaybar.setChecked(value)
        self.ui.tracker.setVisible(value)
        self.cfg.startup['tracker'] = value
        self.cfg.save()

    #@signals.Slot('gui_tables_update')
    def updateFromDB(self):
        """
        Update all anime tables views from database.
        This is used on initialization and after syncronization.
        """
        leafs = {}
        for number, title in LOCAL_STATUS:
            leafs[number] = self.model.findItems(QtCore.QString(number))[0]
        for item in Anime.objects.all():
            status = item.my_status
            if status in leafs.keys():
                leafs[status].appendRow(ACStandardItem(item))

    #@signals.Slot('set_track_message')
    def setTrackMessage(self, message=''):
        self.ui.tracker.setText(message)

    @QtCore.pyqtSlot()
    def sync(self):
        self.manager.sync()
        QtCore.QTimer.singleShot(5000, self, QtCore.SLOT('clearMessage()'))


    @QtCore.pyqtSlot()
    def showAboutDialog(self):
        about = ACAboutDialog(self)
        about.show()

    @QtCore.pyqtSlot()
    def showPreferencesDialog(self):
        pref = ACPreferencesDialog(self)
        pref.show()
