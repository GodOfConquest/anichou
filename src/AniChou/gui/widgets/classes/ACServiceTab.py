

from PyQt4 import QtCore, QtGui

class ACServiceTab(object):

    def __init__(self, parent=None):
        pass

    def setValue(self, value={}):
        self.ui.Username.setValue(value.get('username', ''))
        self.ui.Password.setValue(value.get('password', ''))
        self.ui.enabled.setChecked(bool(value.get('enabled', True)))

    def getValue(self):
        return {
            'username': self.ui.Username.getValue(),
            'password': self.ui.Password.getValue(),
            'enabled': bool(self.ui.enabled.checked())
        }
