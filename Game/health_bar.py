import pygame
from constants import BAR_THICKNESS, BLUE, BRIGHT_RED


class HealthBar:
    def __init__(self, health_object):
        obj_width, obj_height = health_object.rect.size
        bar_x_pos = obj_width * 0.25
        bar_y_pos = obj_height * 0.05
        self.object = health_object
        self.bar_width = obj_width // 2
        self.rect = pygame.Rect((bar_x_pos, bar_y_pos),
                                (self.bar_width, BAR_THICKNESS))
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill(BLUE)

    def change_state(self):
        blue_coef = self.object.health / self.object.max_health
        red_coef = 1.0 - blue_coef
        blue_width = self.bar_width * blue_coef
        red_width = self.bar_width * red_coef
        self.surface.fill(BLUE, (0, 0, blue_width, BAR_THICKNESS))
        self.surface.fill(BRIGHT_RED,
                          (blue_width, 0, red_width, BAR_THICKNESS))
