# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ..ui.Ui_ACTextDialog import Ui_ACTextDialog

class ACTextDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_ACTextDialog()
        self.ui.setupUi(self)

    def setText(self, text):
        self.ui.textEdit.setText(text)

