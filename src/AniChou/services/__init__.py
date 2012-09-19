
import logging

from AniChou import settings
from AniChou.gui import notify
from AniChou.services.default import DefaultService


def chooser(name, classname=None):
    try:
        service = getattr(__import__('AniChou.services.%s' % name,
                fromlist=[name,]), classname or name.capitalize())
    except ImportError, e:
        logging.error(e)
        service = DefaultService
    return service


class Manager(object):

    services = []

    def __init__(self, config):
        self.config = config
        self.main = None
        self.loadServices()

    def loadServices(self):
        """
        Reload all services in manager.
        """
        self.removeService()
        self.addMainService()
        for name in settings.SERVICES:
            if getattr(self.config.services, name).get('enabled'):
                self.addService(name)
        self.updateConfig()

    def addMainService(self):
        """
        Reload main service from config.
        """
        if self.main:
            self.main.stop()
            self.services.remove(self.main)
        service = chooser(self.config.services['default'])
        self.main = service(self.config)
        self.services.append(self.main)

    def addService(self, name):
        """
        Load new service in manager.
        """
        service = chooser(name)
        if type(service) != DefaultService:
            if not filter(lambda s: s.name == service.name, self.services):
                self.services.append(service(self.config))

    def removeService(self, name=None):
        """
        Stop service and unload it from manager.
        Stops all except main if no arguments passed.
        """
        if name:
            service = chooser(name)
            services = filter(lambda s: s.name == service.name, self.services)
        else:
            services = filter(lambda s: s is not self.main, self.services)
        for s in services:
            service.stop()
            self.services.remove(s)

    def sync(self):
        for name in self.syncNext():
            if type(name) == bool:
                if not name:
                    notify('Syncing failed..')
                else:
                    notify('Syncing Done.')
            else:
                notify('Syncing with {0}..'.format(name))

    def syncNext(self):
        """
        This is iterator through all enabled services
        """
        for service in self.services:
            yield service.name
            if not service.sync():
                yield False
        yield True

    def save(self):
        self.main.save()

    def getDb(self):
        """ Compatibility with current gui """
        return self.main.db
    db = property(getDb)

    def updateConfig(self):
        """Reload config"""
        for service in self.services:
            service.setConfig(self.config)
