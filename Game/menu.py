import os
import pygame
import constants
import costs
import buildings
from resources_menu import ResourcesMenu
from unit_menu import UnitMenu


# номер здания, выбранного пользователем
def selected_building_num(mouse_pos, menu_pos, picture_sz):
    mouse_pos_on_menu = mouse_pos[1] - menu_pos[1]
    return (mouse_pos_on_menu - 5) // (picture_sz *
                                       constants.SEPARATION_COEFFICENT)


# функция смены нижнего меню в зависимости от нажатого здания
def state_changing(building_num=None, num=3):
    state = [False] * num
    if building_num is not None:
        state[building_num] = True
    return state


class Menu:  # класс меню
    def __init__(self, picture_sz, pos, gifs, resources):
        picture_pos = 5
        self.picture_sz = picture_sz
        self.pos = pos
        self.height = picture_pos + picture_sz * len(
            gifs) * constants.SEPARATION_COEFFICENT

        # создание поверхности боковой панели
        self.surface = pygame.Surface((picture_sz, self.height))
        self.surface.fill(constants.GREY)

        # создание информационной панели
        screen_width = pygame.display.get_surface().get_size()[0]
        screen_height = pygame.display.get_surface().get_size()[1]
        self.resource_menu = ResourcesMenu(screen_width - picture_sz,
                                           resources)

        # создание юнит-меню
        self.unit_menu_init(screen_width, screen_height, picture_sz)
        self.unit_menu_states = state_changing()
        self.current_state = -1

        # стоимость зданий для их отображения
        self.buildings_cost = (costs.BARRACK_COST, costs.CASTLE_COST,
                               costs.TOWNHALL_COST, costs.STABLE_COST,
                               costs.MARKET_COST, costs.ARCHERY_COST,
                               costs.TOWER_COST, costs.FARM_COST)
        self.cost = pygame.font.SysFont('Calibri', screen_width // 64,
                                        bold=True)

        self.picture_objects = []
        self.text_pos = []
        for i in range(len(gifs)):  # создание картинок
            path = os.path.join(os.getcwd(), 'building_images',
                                gifs[i] + ".png")
            gif = pygame.image.load(path)
            gif.set_colorkey(constants.TRANSPARENT)
            gif = pygame.transform.scale(gif, (picture_sz, picture_sz))
            self.picture_objects.append(gif)
            self.surface.blit(gif, (0, picture_pos))
            self.text_pos.append(picture_pos +
                                 pygame.display.get_surface().get_size()[1] //
                                 23.5)
            self.rendering_text(self.text_pos[i], self.buildings_cost[i])
            picture_pos += picture_sz * constants.SEPARATION_COEFFICENT

    def change_picture_color(self, picture_num,
                             color):  # изменение цвета ячейки в меню
        self.surface.fill(color, (0,
                                  5 + picture_num * self.picture_sz *
                                  constants.SEPARATION_COEFFICENT,
                                  self.picture_sz, self.picture_sz))
        self.surface.blit(self.picture_objects[picture_num],
                          (0,
                           5 + picture_num * self.picture_sz *
                           constants.SEPARATION_COEFFICENT))
        self.rendering_text(self.text_pos[picture_num],
                            self.buildings_cost[picture_num])

    # выделение здания на панели
    def building_selection(self, world, mouse_pos):
        if world.selected_building != -1:
            self.change_picture_color(world.selected_building, constants.GREY)

        # получение номера выбранного здания и выделение его в панели
        world.selected_building = int(
            selected_building_num(mouse_pos, self.pos, self.picture_sz))
        self.picture_objects[world.selected_building].set_colorkey(
            constants.TRANSPARENT)
        self.change_picture_color(world.selected_building, constants.BLUE)

    # нажатие на боковую панель
    def menu_event(self, world, button_key, mouse_pos):
        height = pygame.display.get_surface().get_size()[1]

        if button_key == 1:  # пользователь выбрал тип здания
            self.building_selection(world, mouse_pos)
        elif button_key == 4 and self.pos[1] < 0:  # прокрутка панели
            self.pos[1] += constants.MENU_SPEED
            self.pos[1] = min(0, self.pos[1])
        elif button_key == 5 and self.pos[1] > -self.height + height:
            self.pos[1] -= constants.MENU_SPEED
            self.pos[1] = max(-self.height + height, self.pos[1])

    # получение массива всех картинок
    def get_picture_objects(self):
        return self.picture_objects

    # заливка меню
    def blit(self, screen):
        screen.blit(self.surface, self.pos)
        self.resource_menu.blit(screen)
        self.unit_menu_update(screen)

    # генерация цен на здания
    def rendering_text(self, text_pos, buildings_cost):
        for j in range(len(self.buildings_cost[0])):
            cost_text = self.cost.render(str(buildings_cost[j] * -1),
                                         True, constants.TRANSPARENT)
            self.surface.blit(cost_text, (constants.BUILDING_SIZE // 4,
                                          text_pos))
            text_pos += constants.TEXT_SPACE

    # инициализация меня для созданя юнитов
    def unit_menu_init(self, width, height, picture_sz):
        units_of_buildings = (('ftr3_fr2', 'avt2_fr2'),
                              ('knt1_fr2', 'pdn1_fr1'), ['man1_fr1'])

        unite_menu_height = height // 7
        self.unit_menu = dict()
        for i in range(len(units_of_buildings)):
            unit_menu_sz = (
                len(units_of_buildings[i]) * unite_menu_height,
                unite_menu_height)
            unit_menu_pos = ((width - unit_menu_sz[0] - picture_sz) // 2,
                             height - unit_menu_sz[1])
            self.unit_menu[i] = UnitMenu(unit_menu_sz, unit_menu_pos,
                                         units_of_buildings[i], i)

    # обновление меню созданиея юнитов
    def unit_menu_update(self, screen):
        for state in range(len(self.unit_menu_states)):
            if self.unit_menu_states[state]:
                screen.blit(self.unit_menu[state].surface,
                            self.unit_menu[state].position)

    # выбор конкретного типа нижнего меню
    def current_state_update(self):
        self.current_state = -1
        for state in range(len(self.unit_menu_states)):
            if self.unit_menu_states[state]:
                self.current_state = state

    # определение выбранного здания
    def unit_menu_state_changing(self, world, mouse_pos):
        for building in world.player.building_group:
            if building.rect.collidepoint(mouse_pos):
                if isinstance(building, buildings.Barrack):
                    self.unit_menu_states = state_changing(0)
                    self.unit_menu[0].selected_building = building
                    self.unit_menu[0].change_picture_colour()
                elif isinstance(building, buildings.ArcheryRange):
                    self.unit_menu_states = state_changing(1)
                    self.unit_menu[1].selected_building = building
                    self.unit_menu[1].change_picture_colour()
                elif isinstance(building, buildings.TownHall):
                    self.unit_menu_states = state_changing(2)
                    self.unit_menu[2].selected_building = building
                    self.unit_menu[2].change_picture_colour()

    # проверка нажатия на нижнее меню
    def check_mouse_pos_on_unit_menu(self, mouse_pos):
        if self.current_state == -1:
            return False
        position_one = self.unit_menu[self.current_state].position[1]
        position_two = self.unit_menu[self.current_state].position[0]
        return (mouse_pos[1] > position_one) and \
               (mouse_pos[0] > position_two) and \
               (mouse_pos[0] < self.unit_menu[self.current_state].position[0] +
                self.unit_menu[self.current_state].size[0])
