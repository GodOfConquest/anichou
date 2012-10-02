
import logging

from AniChou import settings
from AniChou import signals
from AniChou.utils import notify
from AniChou.db.models import Anime
from AniChou.services.default import DefaultService


def chooser(name, classname=None):
    if not name:
        return DefaultService
    try:
        service = getattr(__import__('AniChou.services.%s' % name,
                fromlist=[name,]), classname or name.capitalize())
    except ImportError, e:
        logging.error(e)
        service = DefaultService
    return service


class Manager(object):
    ERROR_MESSAGES = {
        'not_found': 'Service {0} not found in loaded services. File skipped.',
    }

    services = []

    def __init__(self, config):
        self.config = config
        self.main = None
        self.loadServices()
        if hasattr(config, 'files'):
            for s, fn in config.files.items():
                try:
                    service = filter(lambda x: x.internalname == s,
                                        self.services)[0]
                except IndexError:
                    logging.warning(ERROR_MESSAGES['not_found'].format(service))
                    continue
                service.loadFile(fn)
            del config['files']
            Anime.objects.save()

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
        signals.emit(signals.Signal('gui_tables_update'))

    def syncNext(self):
        """
        This is iterator through all enabled services
        """
        for service in self.services:
            yield service.name
            try:
                if not service.sync():
                    yield False
            except Exception, e:
                logging.error("""Exception in sync:
{0}""".format(e))
                yield False
        yield True

    def updateConfig(self):
        """Reload config"""
        for service in self.services:
            service.setConfig(self.config)
