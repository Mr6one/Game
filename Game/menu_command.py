import pygame
import constants
from command import Command


class MenuCommand(Command):
    # нажатие на боковую панель
    def event(self, button_key):
        mouse_pos = pygame.mouse.get_pos()
        height = pygame.display.get_surface().get_size()[1]

        if button_key == 1:  # пользователь выбрал тип здания
            self.menu.building_selection(self.world, mouse_pos)
        elif button_key == 4 and self.menu.pos[1] < 0:  # прокрутка панели
            self.menu.pos[1] += constants.MENU_SPEED
            self.menu.pos[1] = min(0, self.menu.pos[1])
        elif button_key == 5 and self.menu.pos[1] > -self.menu.height + height:
            self.menu.pos[1] -= constants.MENU_SPEED
            self.menu.pos[1] = max(-self.menu.height + height,
                                   self.menu.pos[1])
