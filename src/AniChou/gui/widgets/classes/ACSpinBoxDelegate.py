# -*- coding: utf-8 -*

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt


class ACSpinBoxDelegate(QtGui.QItemDelegate):

    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        spin_range = index.data(Qt.DecorationRole).toPyObject()
        editor.setRange(*spin_range)
        return editor

    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole).toPyObject()
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.EditRole)
