import os
import pygame
import costs
import characteristics
from buildings import create_unit_from_building
from help_structures import UnitType
from constants import SEPARATION_COEFFICENT, GREY, BLUE, BLACK, TRANSPARENT


def get_unit_text(building_type):
    unit_types = ([UnitType.SPEAR, UnitType.SWORDSMAN],
                  [UnitType.ARCHER, UnitType.ARBALESTER], [UnitType.SETTLER])
    unit_cost = ((costs.SPEAR_COST, costs.SWORDSMAN_COST),
                 (costs.ARCHER_COST, costs.ARBALESTER_COST),
                 [costs.SETTLER_COST])
    unit_characteristic = ((characteristics.SPEAR, characteristics.SWORDSMAN),
                           (characteristics.ARCHER,
                            characteristics.ARBALESTER),
                           [characteristics.SETTLER])
    return (unit_types[building_type], unit_cost[building_type],
            unit_characteristic[building_type])


class UnitMenu:
    def __init__(self, size, position, gifs, building_type):
        picture_pos = 5
        self.size = size
        self.position = position
        self.state = False
        self.selected_unit = -1
        self.surface = pygame.Surface((self.size[0], self.size[1]))
        self.surface.fill(GREY)
        self.gifs = self.get_unite_pictures(gifs)

        unit_tuple = get_unit_text(building_type)
        self.unit_types, self.unit_cost, self.unit_characteristic = unit_tuple

        self.selected_building = None

        self.vertical_text_pos = [0] * (len(gifs) + 1)
        self.vertical_text_pos[0] = size[1] / 1.5
        screen_width = pygame.display.get_surface().get_size()[0]
        self.cost = pygame.font.SysFont('Calibri', screen_width // 75)

        self.cost_text, self.characteristic_text = \
            self.text_rendering(picture_pos)

    def unit_creation(self, mouse_pos, player):
        if self.selected_unit != -1:
            self.surface.fill(GREY, (
                self.size[1] * self.selected_unit *
                SEPARATION_COEFFICENT, 0, self.size[1],
                self.size[1]))
            self.surface.blit(self.gifs[self.selected_unit],
                              (5 + self.size[1] * self.selected_unit *
                               SEPARATION_COEFFICENT, 40))
            self.text_update()

        self.selected_unit = int(self.selected_unit_num(mouse_pos))
        self.gifs[self.selected_unit].set_colorkey(TRANSPARENT)
        value = self.size[1] * self.selected_unit * SEPARATION_COEFFICENT
        self.surface.fill(BLUE, (value, 0, self.size[1], self.size[1]))
        self.surface.blit(self.gifs[self.selected_unit],
                          (5 + self.size[1] * self.selected_unit *
                           SEPARATION_COEFFICENT, 40))
        self.text_update()

        create_unit_from_building(self.selected_building, player,
                                  self.unit_types[self.selected_unit])

    def change_picture_colour(self):
        self.surface.fill(GREY, (
            self.selected_unit * self.size[1] * SEPARATION_COEFFICENT, 0,
            self.size[1],
            self.size[1]))
        self.surface.blit(self.gifs[self.selected_unit],
                          (5 + self.selected_unit * self.size[1] *
                           SEPARATION_COEFFICENT, 40))

        self.text_update()

    def text_rendering(self, picture_pos):
        for i in range(len(self.gifs)):  # создание картинок
            self.surface.blit(self.gifs[i], (picture_pos, 40))
            horizontal_text_pos = picture_pos
            picture_pos += self.size[1] * SEPARATION_COEFFICENT
            pos = self.size[1] / 3.5

            cost_text = [0] * 3
            characteristic_text = [0] * 3
            for j in range(3):
                cost_text[j] = self.cost.render(str(self.unit_cost[i][j] * -1),
                                                True, BLACK)
                self.surface.blit(cost_text[j], (horizontal_text_pos, 2))
                horizontal_text_pos += self.size[1] // 3

                characteristic_text[j] = self.cost.render(
                    str(self.unit_characteristic[i][j]), True, BLACK)
                self.surface.blit(characteristic_text[j],
                                  (self.vertical_text_pos[i], pos))
                pos += self.size[1] / 5
            vert_pos = self.vertical_text_pos[i]
            self.vertical_text_pos[i + 1] = vert_pos + (picture_pos - 5)
        return cost_text, characteristic_text

    def text_update(self):
        horizontal_text_pos = 5 + (self.size[1] * SEPARATION_COEFFICENT) * \
                              self.selected_unit
        pos = self.size[1] / 3.5
        for j in range(3):
            self.cost_text[j] = self.cost.render(
                str(self.unit_cost[self.selected_unit][j] * -1), True,
                BLACK)
            self.surface.blit(self.cost_text[j],
                              (horizontal_text_pos, 2))
            horizontal_text_pos += self.size[1] // 3

            self.characteristic_text[j] = self.cost.render(
                str(self.unit_characteristic[self.selected_unit][j]),
                True, BLACK)
            self.surface.blit(self.characteristic_text[j],
                              (self.vertical_text_pos[self.selected_unit],
                               pos))
            pos += self.size[1] / 5

    def get_unite_pictures(self, gifs):  # получение массива всех картинок
        picture_objects = []

        for i in range(len(gifs)):
            path = os.path.join(os.getcwd(), 'unit_images', gifs[i] + ".gif")
            gif = pygame.image.load(path)
            gif.set_colorkey(TRANSPARENT)
            print(self.size[1])
            gif = pygame.transform.scale(gif, (self.size[1] - int(self.size[1] / 2),
                                               self.size[1] - int(self.size[1] / 2)))
            picture_objects.append(gif)

        return picture_objects

    def selected_unit_num(self,
                          mouse_pos):  # номер юнита, выбранного пользователем
        mouse_pos_on_menu = mouse_pos[0] - self.position[0]
        return (mouse_pos_on_menu - 5) // (self.size[1] *
                                           SEPARATION_COEFFICENT)
