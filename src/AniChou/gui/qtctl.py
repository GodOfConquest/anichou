
import logging

from PyQt4 import QtCore, QtGui
from AniChou import players, recognizinig
from AniChou import settings
from AniChou.gui.Main import Ui_AniChou
from AniChou.services.data.base import LOCAL_STATUS
from AniChou.gui.widgets import ( ACStatusTab, ACAboutDialog,
                                  ACPreferencesDialog )


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
        self.tracker = QtCore.QTimer()
        self.connect(self.tracker, QtCore.SIGNAL('timeout()'), self.track);
        self.toggleTracker(cfg.startup.get('tracker'))

        self.updateFromDB()


    def notify(self, message):
        self.ui.statusbar.setMessage(message)

    @QtCore.pyqtSlot()
    def clearMessage(self):
        self.ui.statusbar.clearMessage()

    @QtCore.pyqtSlot()
    def sync(self):
        self.manager.sync()
        self.updateFromDB()
        QtCore.QTimer.singleShot(5000, self, QtCore.SLOT('clearMessage()'))

    @QtCore.pyqtSlot(bool)
    def toggleTracker(self, value):
        value = bool(value)
        if value:

            self.tracker.start(settings.TRACKING_INTERVAL)
        else:
            self.tracker.stop()
        self.ui.actionPlaybar.setChecked(value)
        self.ui.tracker.setVisible(value)
        self.cfg.startup['tracker'] = value
        self.cfg.save()

    def track(self):
        if self.ui.tracker.isVisible():
            track = players.get_playing(settings.PLAYERS, self.cfg.search_dirs)
            for key in track.keys():
                e = recognizinig.engine(key, self.manager.db)
                m = e.match()
                try:
                    ep = int(e._getEpisode().strip('/'))
                    if m:
                        if self.manager.db[m]['status_episodes'] == \
                                    ep - 1 and \
                                self.manager.db[m]['status_status'] == \
                                    LOCAL_STATUS_R['watching']:
                            msg = u'Playing: {0} -- Episode: {1}'.format(m, ep)
                            self.ui.tracker.setText(msg)
                            if ep < self.manager.db[m]['episodes']:
                                self.manager.db[m]['status_episodes'] = ep
                                self.manager.db[m]['status_updated'] = \
                                                datetime.datetime.now()
                                self.manager.save()

                                #TODO: it is hack to update table
                                #~ newep = str(ep) + ' / ' + str(self.manager.db[m]['episodes'])
                                #~ sw = self.tv[1].keylist
                                #~ i = 0 # row tracker
                                #~ for key in sw:
                                    #~ if key == m:
                                        #~ break
                                    #~ else:
                                        #~ i += 1
                                #~ self.tv[1].liststore[str(i)][1] = newep
                except:
                    break
        return True

    def updateFromDB(self):
        """
        Update all anime tables views from database.
        This is used on initialization and after syncronization.
        """

        statuses = {}

        # Separate anime data according to their status
        for key, value in self.manager.db.items():
            status = value['status_status']
            if status not in statuses:
                statuses[status] = {}
            status[status][key] = value

        for i in range(0, self._stabs.count()):
            self._stabs.widget(i).updateData(statuses.get(i+1, {}))


    @QtCore.pyqtSlot()
    def sync(self):
        self.manager.sync()
        self.updateFromDB()
        QtCore.QTimer.singleShot(5000, self, QtCore.SLOT('clearMessage()'))


    @QtCore.pyqtSlot()
    def showAboutDialog(self):
        about = ACAboutDialog(self)
        about.show()

    @QtCore.pyqtSlot()
    def showPreferencesDialog(self):
        pref = ACPreferencesDialog(self)
        pref.show()
