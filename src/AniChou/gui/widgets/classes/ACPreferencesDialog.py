
from PyQt4 import QtCore, QtGui
from ..ui.Ui_ACPreferencesDialog import Ui_ACPreferencesDialog

from AniChou import config
from AniChou.gui.widgets import ACServiceTab
from AniChou import settings


class ACPreferencesDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_ACPreferencesDialog()
        self.ui.setupUi(self)
        self.cfg = parent.cfg
        self.ui.tracker.setChecked(bool(self.cfg.startup['tracker']))
        self.ui.sync.setChecked(bool(self.cfg.startup.get('sync')))
        self.ui.searchDirs.setValue(self.cfg.search_dirs)
        for item in settings.SERVICES:
            self.ui.Default_service.addItem(item)
        self.ui.Default_service.setValue(self.cfg.services['default'])
        self.loadServicesTabs()

    def loadServicesTabs(self):
        for name in settings.SERVICES:
            tab = ACServiceTab()
            tab.setValue(getattr(self.cfg.services, name))
            tab.serviceName = name
            self.ui.services.addTab(tab, name)

    def closeEvent(self, event):
        self.saveConfig()

    def saveConfig(self):
        self.cfg.startup['sync'] = bool(self.ui.sync.isChecked())
        self.cfg.startup['tracker'] = bool(self.ui.tracker.isChecked())
        self.cfg.search_dirs = self.ui.searchDirs.getValue()
        self.cfg.services['default'] = self.ui.Default_service.getValue()
        for i in range(0, self.ui.services.count()):
            tab = self.ui.services.widget(i)
            self.cfg.services[tab.serviceName] = tab.getValue()
        self.cfg.save()
