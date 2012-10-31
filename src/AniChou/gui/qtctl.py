# -*- coding: utf-8 -*-

import time

from PyQt4 import QtCore, QtGui
from AniChou import signals
from AniChou.gui.Main import Ui_AniChou
from AniChou.gui.widgets import ( ACAboutDialog, ACPreferencesDialog )
from AniChou.services import ServiceManager


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

        # Sync on start
        if self.cfg.startup.get('sync'):
            QtCore.QTimer.singleShot(100, self, QtCore.SLOT('sync()'))

        # Register signals
        signals.Slot('notify', self.notify)
        signals.Slot('set_track_message', self.setTrackMessage)

        # Setup tracker
        self.tracker = signals.Signal()
        self.tracker.connect('start_tracker')
        self.tracker.connect('stop_tracker')
        self.toggleTracker(cfg.startup.get('tracker'))

        # GUI backend must process application-level signals if it has
        # its own main loop
        self.supportTimer = QtCore.QTimer(self)
        self.connect(self.supportTimer, QtCore.SIGNAL('timeout()'), self.supportThread);
        self.supportTimer.start(0.01)

        # TODO: it must be called from service manager or like
        signals.emit(signals.Signal('gui_tables_update'))


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

    @QtCore.pyqtSlot()
    def newSearch(self):
        text = self.ui.searchBox.text()
        ServiceManager.search(text)
