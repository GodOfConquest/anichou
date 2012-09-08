
from AniChou import settings
from AniChou.services.default import DefaultService


def chooser(name, classname=None):
    try:
        service = getattr(__import__('AniChou.services.%s' % name,
                fromlist=[name,]), classname or name.capitalize())
    except ImportError, e:
        print unicode(e)
        service = DefaultService
    return service


class Manager(object):

    services = []

    def __init__(self, config):
        service = chooser(settings.DEFAULT_SERVICE)
        self.config = config
        self.main = service(config=config)
        self.services.append(self.main)

    def addService(self, name):
        service = chooser(name)
        if type(service) != DefaultService:
            if not filter(lambda s: s.name == service.name, self.services):
                self.services.append(service(self.config))

    def removeService(self, name):
        service = chooser(name)
        services = filter(lambda s: s.name == service.name, self.services)
        for s in services:
            service.stop()
            self.services.remove(s)

    def sync(self):
        """
        This is iterator through all enabled services
        """
        for service in self.services:
            yield service.name
            if not service.sync():
                yield False
        yield u'Done'

    def save(self):
        self.main.save()

    def getDb(self):
        """ Compatibility with current gui """
        return self.main.db
    db = property(getDb)

    def updateConfig(self):
        """Reload config"""
        pass
