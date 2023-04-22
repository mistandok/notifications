import abc

from notify.models import Notify


class SenderProvider(abc.ABC):
    providers = None

    @property
    @abc.abstractmethod
    def provider_name(self):
        pass

    def send(self, data: dict, notify: Notify):
        pass

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]
