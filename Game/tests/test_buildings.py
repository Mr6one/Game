import pytest
from buildings import *
from help_structures import ObjectCollision
import pygame


def test_building_load():
    building_group = pygame.sprite.Group()
    resource_group = pygame.sprite.Group()
    buildings = [Castle, TownHall, Tower, Market, Farm, Barrack, ArcheryRange,
                 Stable]

    for i in range(50):
        for j in range(len(buildings)):
            buildings[j]((j * 300, i * 300), building_group, resource_group)


def test_building_collision():
    with pytest.raises(ObjectCollision):
        building_group = pygame.sprite.Group()
        resource_group = pygame.sprite.Group()

        building_1 = Castle((100, 100), building_group, resource_group)
        building_2 = Castle((100, 100), building_group, resource_group)
