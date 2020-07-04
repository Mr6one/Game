import pygame
from resources import Resources


class Player:
    def __init__(self):
        self.unit_group = pygame.sprite.Group()
        self.building_group = pygame.sprite.Group()
        self.townhalls = pygame.sprite.Group()
        self.resources = Resources()
