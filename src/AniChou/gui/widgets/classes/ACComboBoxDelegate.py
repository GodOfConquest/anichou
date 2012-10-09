

from PyQt4 import QtCore, QtGui


class ACComboBoxDelegate(QtGui.QItemDelegate):

    def __init__(self, parent=None, values=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.setValues(values)

    def setValues(self, values=None):
        self.values = values

    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        if self.values:
            editor.addItems(self.values)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole).toInt()[0]
        editor.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, QtCore.Qt.EditRole)
