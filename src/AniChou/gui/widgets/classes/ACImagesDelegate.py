# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QStyle, QApplication
from AniChou.gui.widgets import ACReadOnlyDelegate
from AniChou.services import ServiceManager

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


IMAGES_CACHE = {}


def create_image(name):
    service = ServiceManager.getService(name)
    path = ''
    if service:
        path = service.image
    pixmap = QtGui.QImage(_fromUtf8(path))
    IMAGES_CACHE[name] = pixmap
    return pixmap



class ACImagesDelegate(ACReadOnlyDelegate):

    padding = 5

    def paint(self, painter, option, index):
        images = index.data().toPyObject()
        if not images:
            return

        pleft = 0
        for key, link in images.items():
            rect = QtCore.QRect(option.rect)
            image = IMAGES_CACHE.get(key)
            if not image:
                image = create_image(key)
            pleft += self.padding
            ptop = (rect.height() - image.height()) / 2
            rect.translate(pleft, ptop)
            pleft += image.height()
            painter.drawImage(rect.topLeft(), image)





