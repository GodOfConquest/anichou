
import logging
import cStringIO
import traceback


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
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    msg = '\n'.join([errmsg, tbinfo])
    logging.error(msg)
