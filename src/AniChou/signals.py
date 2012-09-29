
import types
from Queue import Queue
from functools import partial
from weakref import WeakValueDictionary


__all__ = ['Slot', 'Signal', 'emit', 'process']

registred_slots = WeakValueDictionary()
signals_stack = Queue()



class Slot(object):
    """
    This decorator register slot for use by signals
    """
    def __init__(self, name=None):
        self.name = name

    def __call__(self, func):
        def wrapped_f(*args, **kwargs):
            func(*args, **kwargs)
        # Check slot name and add to dict
        if not self.name:
            self.name = '.'.join(func.__module__, func.__name__)
        registred_slots[self.name] = wrapped_f
        return wrapped_f


class Signal(object):
    def __init__(self, *args):
        self.__slots = WeakValueDictionary()
        for slot in args:
            self.connect(slot)

    def __call__(self, slot, *args, **kwargs):
        """
        Emit signal. If slot passed signal will be called only for this
        slot, for all connected slots otherwise.

        Calling this method directly lead to immediate signal processing.
        It may be not thread-safe. Use emit method from this module for
        delayed calling of signals.
        """
        if slot is not None:
            slots = (self.__slots[self.key(slot)],)
        else:
            slots = self.__slots.values()
        for func in slots:
            func(*args, **kwargs)

    def key(self, slot):
        """
        Get local key name for slot.
        """
        if type(slot) == types.FunctionType:
            key = (slot.__module__, slot.__name__)
        elif type(slot) == types.MethodType:
            key = (slot.__func__, id(slot.__self__))
        elif isinstance(slot, basestring):
            if not slot in registred_slots.keys():
                raise ValueError('Slot {0} does not exists.'.format(slot))
            key = slot
        else:
            raise ValueError('Slot {0} has non-slot type'.format(slot))
        return key

    def connect(self, slot):
        """
        Connect signal to slot. Slot may be function, instance method
        or name of function perviously registred by `slot` decorator.
        """
        key = self.key(slot)
        if type(slot) == types.FunctionType:
            self.__slots[key] = slot
        elif type(slot) == types.MethodType:
            self.__slots[key] = partial(slot.__func__, slot.__self__)
        elif isinstance(slot, basestring):
            self.__slots[key] = registred_slots[slot]

    def disconnect(self, slot):
        """
        Remove slot from signal connetions.
        """
        key = self.key(slot)
        del self.__slots[key]

    def clear(self):
        """
        Disconnect all slots from signal.
        """
        self.__slots.clear()


def emit(signal, slot, *args, **kwargs):
    """
    Takes signal and adds it to signal queue.
    """
    prepared = partial(signal, slot, *args, **kwargs)
    signals_stack.put_nowait(prepared)


def process():
    """
    Call all signals in queue.
    """
    while not signals_stack.empty():
        signal = signals_stack.get_nowait()
        signal()
