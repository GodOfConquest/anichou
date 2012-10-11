# -*- coding: utf-8 -*-

from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt
from AniChou.gui.widgets import ACReadOnlyDelegate


class ACColorDelegate(ACReadOnlyDelegate):

    def paint(self, painter, option, index):
        color = QColor(*index.data(Qt.DecorationRole).toPyObject())
        painter.fillRect(option.rect, color)
