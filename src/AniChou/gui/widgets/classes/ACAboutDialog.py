# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore, QtGui

from ..ui.Ui_ACAboutDialog import Ui_ACAboutDialog

from AniChou import settings
from AniChou.gui.widgets import ACTextDialog


class ACAboutDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_ACAboutDialog()
        self.ui.setupUi(self)
        self.license = None
        self.credits = None

    @QtCore.pyqtSlot()
    def credits(self):
        if not self.credits:
            self.credits = ACTextDialog(self)
            self.credits.setText(open(os.path.join(settings.PACKAGE_PATH,
                                            'data', 'AUTHORS')).read())
        self.credits.show()

    @QtCore.pyqtSlot()
    def license(self):
        if not self.license:
            self.license = ACTextDialog(self)
            self.license.setText(open(os.path.join(settings.PACKAGE_PATH,
                                            'data', 'COPYING')).read())
        self.license.show()


