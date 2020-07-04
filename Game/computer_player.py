import random
import pygame
import buildings
from buildings import create_unit_from_building
from player import Player
from help_structures import UnitType, ObjectCollision
from constants import FPS, CASTLE_SIZE
from squad import Army


class Bot(Player):  # класс компьютерного игрока
    def __init__(self, base_position, world):
        super().__init__()
        self.resources.change_values(1000000, 1000000, 1000000)

        # позиция, вокруг которой создаются здания
        self.base_position = base_position

        # характеристика готовности бота к созданию юнита или здания
        # обновляется при каждом
        self.creation_state = 1
        self.max_state = FPS * 300
        self.main_building = ('townhall')
        self.creation_buildings = ('barrack', 'archery_range')
        self.other_buildings = ('castle', 'stable', 'market', 'tower', 'farm')

        self.creation_building_group = pygame.sprite.Group()

        # отряды бота
        self.cur_squad = Army()
        self.squads = list()

        first_building = buildings.TownHall(self.base_position,
                                            self.building_group,
                                            world.resource_group)
        first_building.add(self.townhalls)

    # создание здания
    def create_building(self, building_names, world):
        x_pos = self.base_position[0]
        y_pos = self.base_position[1]
        field_width = world.field.get_size()[0]
        new_building: buildings.Building = None
        while True:
            try:
                new_building = \
                    buildings.create_building(random.choice(building_names),
                                              (x_pos, y_pos), self,
                                              world.resource_group)

                break
            except ObjectCollision:
                x_pos += CASTLE_SIZE * random.randint(-1, 1)
                y_pos += CASTLE_SIZE * random.randint(-1, 1)
            if x_pos > field_width:
                x_pos -= CASTLE_SIZE * 4
            if y_pos > field_width:
                y_pos -= CASTLE_SIZE * 4

        return new_building

    # создание юнитов
    def create_units(self):
        for building in self.creation_building_group:
            if isinstance(building, buildings.Barrack):
                unit = create_unit_from_building(building, self,
                                                 random.choice(
                                                     (UnitType.SWORDSMAN,
                                                      UnitType.SPEAR)))
            elif isinstance(building, buildings.ArcheryRange):
                unit = create_unit_from_building(building, self,
                                                 random.choice(
                                                     (UnitType.ARCHER,
                                                      UnitType.ARBALESTER)))
            else:
                continue
            self.cur_squad.add(unit)

    # в зависимости от состояния бот создаёт те или иные объекты раз в
    # какой-то промежуток времени
    def bot_event(self, world):
        # каждый 5 минут новое главное здание
        if self.creation_state == self.max_state:
            building = self.create_building(self.main_building, world)
            building.add(self.townhalls)

        # каждую минуту новое здание, создающее юнитов
        if self.creation_state % (self.max_state / 5) == 0:
            building = self.create_building(self.creation_buildings, world)
            building.add(self.creation_building_group)

        # каждую минуту все юниты атакуют главное здание врага
        if self.creation_state % (self.max_state / 5) == 0:
            self.squads.append(self.cur_squad)
            townhall = world.player.townhalls.sprites()[0]
            for squad in self.squads:
                squad.set_goal(townhall.rect.center)
            self.cur_squad = Army()

        # каждую минуту какое-то другое новое здание
        if self.creation_state % (self.max_state / 5) == self.max_state / 10:
            self.create_building(self.other_buildings, world)

        # каждые 5 секунд новый юнит около каждого здания
        if self.creation_state % (self.max_state / 60) == 0:
            self.create_units()

        # меняем состояние бота
        self.creation_state = (self.creation_state + 1) % self.max_state
