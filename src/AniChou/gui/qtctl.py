
import logging
import time

from PyQt4 import QtCore, QtGui
from AniChou import players, recognizinig
from AniChou import settings
from AniChou import signals
from AniChou.db.models import Anime
from AniChou.gui.Main import Ui_AniChou
from AniChou.gui.widgets import ( ACStatusTab, ACAboutDialog,
                                  ACPreferencesDialog )
from AniChou.services.data.base import LOCAL_STATUS


__all__ = ['get_app', 'Main']


def get_app(argv):
    return QtGui.QApplication(argv)


class SupportThread(QtCore.QThread):
    """
    This thread does all application additional logic like processing
    application-level signals.
    """
    _exit = False
    def run(self):
        while not self._exit:
            signals.process()
            time.sleep(0.01)


class Main(QtGui.QMainWindow):

    def __init__(self, manager, cfg):
        self.manager = manager
        self.cfg = cfg
        self.supportThread = SupportThread()
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_AniChou()
        self.ui.setupUi(self)
        self._stabs = self.ui.statusTabs

        # Create tabs
        for number, title in LOCAL_STATUS[1:]:
            tab = ACStatusTab(self._stabs)
            self._stabs.addTab(tab, title)
            tab.status = number

        # Sync on start
        if self.cfg.startup.get('sync'):
            QtCore.QTimer.singleShot(100, self, QtCore.SLOT('sync()'))

        # Setup tracker
        self.tracker = signals.Signal()
        self.tracker.connect('start_tracker')
        self.tracker.connect('stop_tracker')
        self.toggleTracker(cfg.startup.get('tracker'))
        self.updateFromDB()
        self.supportThread.start()


    @signals.Slot('notify')
    def notify(self, message):
        self.ui.statusbar.setMessage(message)

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

    @signals.Slot('gui_tables_update')
    def updateFromDB(self):
        """
        Update all anime tables views from database.
        This is used on initialization and after syncronization.
        """

        statuses = {}
        # Separate anime data according to their status
        for item in Anime.objects.all():
            status = item.my_status
            if status not in statuses:
                statuses[status] = []
            statuses[status].append(item)

        for i in range(0, self._stabs.count()):
            self._stabs.widget(i).updateData(statuses.get(i+1, {}))

    @signals.Slot('set_track_message')
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
