import pygame
import constants


class Block:
    def __init__(self, width, height, x_pos, name):
        self.surface = pygame.Surface((width, height))
        self.surface.fill(constants.GREY)
        self.x_pos = x_pos
        self.resource_name = name
        self.gold_text = pygame.font.SysFont('Calibri', height)

    def update(self, resource_value):
        self.surface.fill(constants.GREY)
        text = self.resource_name + ": " + str(resource_value)
        text = self.gold_text.render(text, False, constants.BLUE)
        self.surface.blit(text, (10, 2))
