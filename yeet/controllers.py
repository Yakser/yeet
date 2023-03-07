from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def render(self, request, path):
        pass
