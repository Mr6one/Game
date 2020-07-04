from enum import Enum


class ObjectCollision(Exception):  # исключение коллизии объектов
    pass


class Direction(Enum):  # направление движение юнита
    NONE = 0
    LEFT = 1
    RIGHT = 2
    FRONT = 3
    BACK = 4


class UnitType(Enum):  # тип юнита
    SPEAR = 0
    SWORDSMAN = 1
    ARCHER = 2
    ARBALESTER = 3
    SETTLER = 4


class ResourceType(Enum):
    FOOD = 0
    GOLD = 1
    WOOD = 2


class GameState(Enum):
    PLAYER_WIN = 0
    PLAYER_LOSE = 1
    GAME_CONTINUE = 2
