# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QStyle, QApplication
from AniChou.gui.widgets import ACReadOnlyDelegate


class ACProgressBarDelegate(ACReadOnlyDelegate):

    def paint(self, painter, option, index):
        # Set up a QStyleOptionProgressBar to precisely mimic the
        # environment of a progress bar.
        progressBarOption = QtGui.QStyleOptionProgressBarV2();
        progressBarOption.state = QStyle.State_Enabled;
        progressBarOption.direction = QApplication.layoutDirection();
        progressBarOption.rect = option.rect;
        progressBarOption.fontMetrics = QApplication.fontMetrics();
        progressBarOption.minimum = 0;
        progressBarOption.maximum = 100;
        progressBarOption.textAlignment = QtCore.Qt.AlignCenter;
        progressBarOption.textVisible = True;

        # Set the progress and text values of the style option.
        #progress = (parent())->clientForRow(index.row())->progress();
        progress = index.data().toPyObject()
        progressBarOption.progress = 0 if progress < 0 else progress
        progressBarOption.text = QtCore.QString("{0}%".format(progressBarOption.progress));

        # Draw the progress bar onto the view.
        QApplication.style().drawControl(QStyle.CE_ProgressBar, progressBarOption, painter);
