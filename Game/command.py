from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, world, menu):
        self.world = world
        self.menu = menu

    @abstractmethod
    def event(self, button_key):
        pass
