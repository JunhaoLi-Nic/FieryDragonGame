# Imports
from abc import ABC, abstractmethod


class ActionCapable(ABC):

    @abstractmethod
    def execute(self):
        pass
