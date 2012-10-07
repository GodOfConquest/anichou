
from PyQt4 import QtCore, QtGui


class ACSpinBoxDelegate(QtGui.QItemDelegate):

    def __init__(self, parent=None, spin_range=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.range = spin_range

    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        if self.range and len(self.range) == 2:
            editor.setRange(*self.range)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole).toInt()[0]
        editor.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, QtCore.Qt.EditRole)
