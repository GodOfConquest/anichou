# -*- coding: utf-8 -*-

import sys
import subprocess
import webbrowser
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QStyle, QApplication
from PyQt4.QtCore import QEvent
from AniChou.gui.widgets import ACReadOnlyDelegate
from AniChou.services import ServiceManager

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


IMAGES_CACHE = {}


def open_url(url):
    """Opens the webbrowser and goes to the given url."""
    if sys.platform.startswith('linux'):
        subprocess.call(['xdg-open', url])
    else:
        webbrowser.open(url)


def create_image(name):
    service = ServiceManager.getService(name)
    path = ''
    link = ''
    if service:
        path = service.image
        link = service.cardURL()
    pixmap = QtGui.QImage(_fromUtf8(path))
    IMAGES_CACHE[name] = (pixmap, link)
    return (pixmap, link)



class ACImagesDelegate(ACReadOnlyDelegate):

    padding = 5  # Space between images
    _images = [] # Store rects of all images

    def paint(self, painter, option, index):
        images = index.data().toPyObject()
        if not images:
            return

        del self._images[:]

        pleft = 0
        for key, link_id in images.items():
            rect = QtCore.QRect(option.rect)
            try:
                image, link = IMAGES_CACHE.get(key)
            except:
                image, link = create_image(key)
            link = link.format(link_id)
            # Add padding to offset
            pleft += self.padding
            ptop = (rect.height() - image.height()) / 2
            # Set rect top left point
            rect.translate(pleft, ptop)
            rect.setWidth(image.width())
            rect.setHeight(image.height())
            self._images.append((link, rect))
            painter.drawImage(rect.topLeft(), image)
            # Add image size to total offset
            pleft += image.height()

    def drawDisplay(self, painter, option, rect, text):
        print '1'

    def editorEvent(self, event, model, option, index):
        if event.type() not in [QEvent.MouseButtonRelease, ]:
            return False
        epos = event.pos()
        for link, rect in self._images:
            if not rect.contains(epos):
                continue
            open_url(link)
            return True
        return False



