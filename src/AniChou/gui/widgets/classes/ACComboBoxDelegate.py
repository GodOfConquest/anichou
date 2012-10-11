# -*- coding: utf-8 -*

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt


class ACComboBoxDelegate(QtGui.QItemDelegate):

    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        values = index.data(Qt.DecorationRole).toPyObject()
        editor.addItems(values)
        return editor

    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole).toPyObject()
        value = editor.findText(str(value))
        if value >= 0:
            editor.setCurrentIndex(value)

    def setModelData(self, editor, model, index):
        value = str(editor.currentText())
        model.setData(index, value, Qt.EditRole)
