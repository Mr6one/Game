import pygame
from command import Command


# нажатие на клавишу клавиатуры
class UnitMenuCommand(Command):
    def event(self, button_key):
        mouse_pos = pygame.mouse.get_pos()
        if button_key == 1:
            current_state = self.menu.current_state
            self.menu.unit_menu[current_state].unit_creation(mouse_pos,
                                                             self.world.player)
