# -*- coding: utf-8 -*-

import cStringIO
import logging
import traceback
from AniChou import signals
from urllib2 import Request as URLRequest


class ACRequest(URLRequest):
    def __init__(self, *args, **kwargs):
        self._method = kwargs.pop('method', None)
        URLRequest.__init__(self, *args, **kwargs)

    def get_method(self):
        return self._method if self._method else \
                    URLRequest.get_method(self)


class classproperty(property):
    def __get__(self, obj, type_):
        return self.fget.__get__(None, type_)()

    def __set__(self, obj, value):
        cls = type(obj)
        return self.fset.__get__(None, cls)(value)


def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    notice = \
        """An unhandled exception occurred. Please report the problem\n"""\
        """Error information:\n"""

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = u'{0}: \n{1}'.format(excType, excValue)
    msg = u'\n'.join([errmsg, tbinfo])
    logging.error(msg)


def notify(message):
    logging.info(message)
    signals.emit(signals.Signal('notify'), None, message)
