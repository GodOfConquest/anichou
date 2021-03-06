# -*- coding: utf-8 -*-

import logging
import re

from PyQt4 import QtCore, QtGui


abstract_classes = ['ACReadOnlyDelegate', 'ACSpinBoxDelegate',
        'ACComboBoxDelegate', 'ACProgressBarDelegate', 'ACColorDelegate',
        'ACImagesDelegate', 'ACStandardItem', 'ACStandardItemModel',
        'ACSortFilterProxyModel']

export_classes = ['ACServiceTab', 'ACSimpleInputWidget', 'ACComboBoxWidget']

extern_classes = ['ACStatusTab', 'ACTabWidget', 'ACDirectoryListWidget',
                  'ACTextDialog', 'ACAboutDialog', 'ACPreferencesDialog']


def widget_factory(name):
    try:
        parent_class = getattr(__import__('{0}.classes.{1}'.format(__name__, name),
                    globals(), locals(), [name,]), name)
    except ImportError, e:
        logging.error(e)
        parent_class = QtCore.QObject
    if not issubclass(parent_class, QtGui.QWidget):
        main_class = QtGui.QWidget
    else:
        main_class = QtCore.QObject
    if issubclass(parent_class, main_class):
        first_class, second_class = parent_class, main_class
    else:
        first_class, second_class = main_class, parent_class
    class _ACAbstractWidget(first_class, second_class):
        def __init__(self, parent = None):
            main_class.__init__(self, parent)
            ui = __import__('ui.Ui_' + name, globals(), fromlist=[name,])
            self.ui = getattr(ui, 'Ui_' + name)()
            self.ui.setupUi(self)
            #parent executes after all things done
            parent_class.__init__(self, parent)

        def setObjectName(self, name):
            super(_ACAbstractWidget, self).setObjectName(name)
            try:
                l = filter(lambda x: type(x) == QtGui.QLabel,
                self.children())[0]
                t = re.sub('_\d+$', '', unicode(self.objectName()))
                t = re.sub('_', ' ', t)
                l.setText(t + ':')
            except IndexError:
                pass

        def getValue(self):
            try:
                return super(_ACAbstractWidget, self).getValue()
            except AttributeError:
                pass
            ret = []
            lines = filter(lambda x: type(x) in [QtGui.QLineEdit,
                        QtGui.QSpinBox, QtGui.QDoubleSpinBox,
                        QtGui.QCheckBox, QtGui.QComboBox],
                        self.children())
            for line in lines:
                ltype = type(line)
                t = ''
                if ltype == QtGui.QLineEdit:
                    t = unicode(line.text())
                    if re.match("^\d+\.\d+$", t, re.U):
                        t = float(t)
                    elif re.match("^\d+$", t):
                        t = int(t)
                elif ltype == QtGui.QSpinBox:
                    t = int(line.value())
                elif ltype == QtGui.QDoubleSpinBox:
                    t = float(line.value())
                elif ltype == QtGui.QCheckBox:
                    t = bool(line.isChecked())
                elif ltype == QtGui.QComboBox:
                    t = unicode(line.currentText())
                ret.append(t)
            if not len(ret):
                return
            if len(ret) < 2:
                ret = ret[0]
            return ret

        def setValue(self, *data):
            try:
                return super(_ACAbstractWidget, self).setValue(*data)
            except AttributeError:
                pass
            lines = filter(lambda x: type(x) in [QtGui.QLineEdit,
                            QtGui.QSpinBox, QtGui.QDoubleSpinBox,
                            QtGui.QCheckBox, QtGui.QComboBox],
                            self.children())
            if len(lines):
                values = []
                if type(data) not in (list, tuple):
                    data = [data,]
                for i in range(0, len(lines)):
                    ltype = type(lines[i])
                    field = ''
                    if i < len(data):
                        field = data[i]
                    if ltype == QtGui.QLineEdit:
                        field = unicode(field)
                        lines[i].setText(field)
                    elif ltype == QtGui.QSpinBox:
                        if not field:
                            field = 0
                        try:
                            field = int(field)
                            lines[i].setValue(field)
                        except:
                            pass
                    elif ltype == QtGui.QDoubleSpinBox:
                        if not field:
                            field = 0.0
                        field = float(field)
                        lines[i].setValue(field)
                    elif ltype == QtGui.QCheckBox:
                        field = bool(field)
                        if not field:
                            field = False
                        lines[i].setChecked(field)
                    elif ltype == QtGui.QComboBox:
                        field = lines[i].findText(unicode(field))
                        if field >= 0:
                            lines[i].setCurrentIndex(field)
                    values.append(field if type(field) is not unicode else QtCore.QString(field))
                self._changed(*values)

        def _changed(self, *values):
            types = ', '.join(map(lambda x: type(x).__name__, values))
            self.emit(QtCore.SIGNAL("valueChanged(%s)" % types), *values)

    return _ACAbstractWidget


def load_exports(name):
    globals()[name] = widget_factory(name)


def load_extern(name):
    globals()[name] = getattr(__import__('{0}.classes.{1}'.format(
                            __name__, name), fromlist=[name,]), name)


for name in abstract_classes:
    load_extern(name)
for name in export_classes:
    load_exports(name)
for name in extern_classes:
    load_extern(name)

__all__ = abstract_classes + export_classes + extern_classes
