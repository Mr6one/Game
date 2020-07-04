from abc import ABC, abstractmethod


class Squad(ABC):
    def __init__(self):
        self._parent = self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def add(self, squad):
        pass

    def remove(self, squad):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def set_goal(self, goal):
        pass

    @abstractmethod
    def increase_health(self, additional_health):
        pass


class Army(Squad):
    def __init__(self):
        super().__init__()
        self._children = []

    def add(self, squad: Squad):
        self._children.append(squad)
        squad.parent = self

    def remove(self, squad: Squad):
        self._children.remove(squad.component)
        squad.component.parent = None

    def move(self):
        for child in self._children:
            child.move()

    def set_goal(self, goal):
        for child in self._children:
            child.set_goal(goal)

    def increase_health(self, additional_health):
        pass
