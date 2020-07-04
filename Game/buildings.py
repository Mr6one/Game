import os
import random
import pygame
import units
from help_structures import UnitType, ObjectCollision
from constants import CASTLE_SIZE, BUILDING_SIZE, UNIT_SIZE
from health_bar import HealthBar
from player import Player
from costs import TOWNHALL_COST, CASTLE_COST, STABLE_COST, MARKET_COST, \
    BARRACK_COST, ARCHERY_COST, TOWER_COST, FARM_COST


def create_unit_from_building(building, player: Player,
                              unit_type):  # создание юнита около здания
    x_pos = building.rect[0] + building.rect[2] // 2
    y_pos = building.rect[1] + building.rect[3] // 2
    unit: units.Unit = None
    while True:
        try:
            unit = building.create_unit((x_pos, y_pos), player, unit_type)
            break
        except ObjectCollision:
            x_pos += UNIT_SIZE * random.randint(-1, 1)
            y_pos += UNIT_SIZE * random.randint(-1, 1)

    return unit


def create_building(building_name, mouse_pos,
                    player, resource_group):  # создание нужного здания
    buildings_obj = [Barrack, Castle, TownHall, Stable, Market, ArcheryRange,
                     Tower, Farm]
    names = ['barrack', 'castle', 'townhall', 'stable', 'market',
             'archery_range', 'tower', 'farm']
    costs = [BARRACK_COST, CASTLE_COST, TOWNHALL_COST, STABLE_COST,
             MARKET_COST, ARCHERY_COST, TOWER_COST, FARM_COST]
    for building, name, cost in zip(buildings_obj, names, costs):
        if building_name == name:
            try:
                if player.resources.check_values(*cost):
                    new_build = building(mouse_pos, player.building_group,
                                         resource_group)
                    player.resources.change_values(*cost)
                    if name == 'townhall':
                        new_build.add(player.townhalls)
                    return new_build
            except ObjectCollision:
                raise ObjectCollision

    return None


class Building(pygame.sprite.Sprite):  # класс строения
    def __init__(self, image_name, pos, groups,
                 size=(BUILDING_SIZE, BUILDING_SIZE)):
        pygame.sprite.Sprite.__init__(self)
        path = os.path.join(os.getcwd(), 'building_images', image_name)
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=pos)

        if pygame.sprite.spritecollideany(self, groups[0]) is not None:
            raise ObjectCollision

        if pygame.sprite.spritecollideany(self, groups[1]) is not None:
            raise ObjectCollision

        self.add(groups[0])
        self.health_bar = HealthBar(self)
        self.health = self.max_health = 50000.0
        self.level = 1
        self.damage_coef = 1.0
        self.image.blit(self.health_bar.surface, self.health_bar.rect)

    def increase_health(self, additional_health):  # восстановление здоровья
        self.health += additional_health
        self.health = min(self.health, self.max_health)

    def decrease_health(self, damage):  # нанесение урона
        self.health -= damage * self.damage_coef
        if self.health <= 0.0:
            self.damage()

    def update(self):
        self.increase_health(1.0)
        self.health_bar.change_state()
        self.image.blit(self.health_bar.surface, self.health_bar.rect)

    def build_update(self):  # прокачка строения
        self.level += 1
        self.unit_creator.increase_creation_spped()

    def damage(self):
        self.kill()


class Castle(Building):  # крепость
    def __init__(self, pos, group, resource_group):
        super().__init__("castle.png", pos, (group, resource_group),
                         (CASTLE_SIZE, CASTLE_SIZE))
        self.health = self.max_health = 70000.0
        self.damage_coef = 0.8


class TownHall(Building):  # ратуша
    def __init__(self, pos, group, resource_group):
        super().__init__("townhall.png", pos, (group, resource_group))
        self.health = self.max_health = 100000.0
        self.settler_creator: units.UnitCreator = units.SettlerCreator()

    def create_unit(self, pos, player,
                    unit_type: UnitType):  # создание поселенца
        if unit_type == UnitType.SETTLER:
            return self.settler_creator.create_unit(pos, player)
        return None


class Tower(Building):  # башня
    def __init__(self, pos, group, resource_group):
        super().__init__("tower.png", pos, (group, resource_group))


class Market(Building):  # рынок
    def __init__(self, pos, group, resource_group):
        super().__init__("market.png", pos, (group, resource_group))


class Farm(Building):  # ферма
    def __init__(self, pos, group, resource_group):
        super().__init__("farm.png", pos, (group, resource_group))


class Barrack(Building):  # баррак
    def __init__(self, pos, group, resource_group):
        super().__init__("barrack.png", pos, (group, resource_group))
        self.health = self.max_health = 60000.0
        self.swordsman_creator: units.UnitCreator = units.SwordsmanCreator()
        self.spear_creator: units.UnitCreator = units.SpearCreator()

    # создание мечника или копейщика
    def create_unit(self, pos, player, unit_type: UnitType):
        if unit_type == UnitType.SWORDSMAN:
            return self.swordsman_creator.create_unit(pos, player)

        return self.spear_creator.create_unit(pos, player)


class ArcheryRange(Building):  # тир
    def __init__(self, pos, group, resource_group):
        super().__init__("archery_range.png", pos, (group, resource_group))
        self.archer_creator: units.UnitCreator = units.ArcherCreator()
        self.arbalester_creator: units.UnitCreator = units.ArbalesterCreator()

    # создание лучника или арбалетчика
    def create_unit(self, pos, player, unit_type: UnitType):
        if unit_type == UnitType.ARCHER:
            return self.archer_creator.create_unit(pos, player)

        return self.arbalester_creator.create_unit(pos, player)


class Stable(Building):  # конюшня
    def __init__(self, pos, group, resource_group):
        super().__init__("stable.png", pos, (group, resource_group))
