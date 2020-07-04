import pygame
import buildings
import constants
from command import Command
from help_structures import ObjectCollision


# нажатие на игровое поле
class FieldCommand(Command):
    def event(self, button_key):
        # массив названий зданий
        buildings_names = ['barrack', 'castle', 'townhall', 'stable', 'market',
                           'archery_range', 'tower', 'farm']

        field_pos = self.world.get_field_pos()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] + field_pos[0], mouse_pos[1] + field_pos[1])
        if button_key == 1:
            if self.world.selected_building != - 1:  # создаём здание на поле
                try:
                    # здания на территории бота создавать нельзя!
                    mouse_check = mouse_pos[1] * constants.FIELD_WIDTH < \
                                  constants.FIELD_HEIGHT * \
                                  (-mouse_pos[0] + constants.FIELD_WIDTH)
                    if mouse_check:
                        buildings.create_building(
                            buildings_names[self.world.selected_building],
                            mouse_pos, self.world.player,
                            self.world.resource_group)
                except ObjectCollision:
                    print("Коллизия")
            elif self.world.new_army is not None:
                self.world.new_army = None

            self.menu.unit_menu_state_changing(self.world, mouse_pos)
        elif button_key == 3:  # сбрасываем выделение на боковой панели
            for i in range(len(self.menu.unit_menu)):
                if self.menu.unit_menu[i].selected_unit != -1:
                    self.menu.unit_menu[i].change_picture_colour()
            if self.world.selected_building != -1:
                self.menu.change_picture_color(self.world.selected_building,
                                               constants.GREY)
                self.world.selected_building = -1
            elif self.world.new_army is not None:
                self.world.new_army.set_goal((mouse_pos[0], mouse_pos[1]))
            self.world.selected_building = -1
