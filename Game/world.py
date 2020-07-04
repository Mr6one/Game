import random
import pygame
import constants
import units
from camera import Client, Camera, camera_configure
from computer_player import Bot
from player import Player
from help_structures import ResourceType, ObjectCollision, UnitType, GameState
from resources_sprite import ResourcesSprite
from buildings import create_unit_from_building, TownHall


class World:  # основной класс игры, содержащий все объекты игрового мира
    def __init__(self, field_window_width, screen):
        self.screen = screen
        self.selected_building = -1
        self.player = Player()
        self.new_army = None
        self.field = pygame.Surface((4000, 4000))
        self.field.fill(constants.GREEN)
        self.field_window_width = field_window_width
        self.field_window_height = pygame.display.get_surface().get_size()[1]

        # динамическая камера
        field_size = self.field.get_size()
        total_level_width = field_size[0] - self.field_window_width
        total_level_height = field_size[1] - self.field_window_height
        self.client = Client(0, 0, total_level_width, total_level_height)
        self.camera = Camera(camera_configure, total_level_width,
                             total_level_height, (field_window_width,
                                                  self.field_window_height))

        # генерация ресурсов
        self.resource_state = 0
        self.resource_sprites_generation(field_size)

        # главное здание игрока
        townhall = TownHall((field_size[0] // 8, field_size[0] // 10),
                            self.player.building_group, self.resource_group)
        townhall.add(self.player.townhalls)
        for i in range(constants.START_UNITS_NUM):
            if i == -1:
                break
            create_unit_from_building(townhall, self.player, UnitType.SETTLER)

        # создаём противника
        self.bot = Bot((self.field.get_size()[0] * 3 // 4,
                        self.field.get_size()[1] * 3 // 4), self)

    # генерация ресурсов
    def resource_sprites_generation(self, field_size):
        self.resource_group = pygame.sprite.Group()
        image_resource = ['sheep.png', 'goldmine.png', 'tree.png']
        self.resource_sprites = list()
        sizes = [(constants.SHEEP_SIZE, constants.SHEEP_SIZE),
                 (constants.MINE_SIZE, constants.MINE_SIZE),
                 (constants.TREE_SIZE, constants.TREE_SIZE)]
        resources_type = [ResourceType.FOOD, ResourceType.GOLD,
                          ResourceType.WOOD]

        for i in range(len(resources_type)):  # по 5 ресурсов каждого типа
            for count in range(constants.RESOURCE_NUMBER):
                if count == -1:
                    break
                try:
                    pos = (random.randint(field_size[0] // 4, field_size[0]),
                           random.randint(field_size[1] // 4,
                                          field_size[1] // 2))
                    new_sprite = ResourcesSprite(self.resource_group,
                                                 image_resource[i],
                                                 pos, sizes[i],
                                                 resources_type[i])
                    self.resource_sprites.append(new_sprite)
                except ObjectCollision:
                    pass

    def update(self):  # обновление мира
        self.bot.bot_event(self)  # бот 'делает свой ход'
        max_res = constants.MAX_RESOURCES
        self.resource_state = (self.resource_state + 1) % max_res
        self.resource_update()

        # перезаливка поля
        self.field.fill(constants.GREEN, (self.client.rect.x,
                                          self.client.rect.y,
                                          self.field_window_width,
                                          self.field_window_height))
        pygame.draw.line(self.field, constants.TRANSPARENT,
                         (0, constants.FIELD_WIDTH),
                         (constants.FIELD_HEIGHT, 0), 10)

        for unit in self.player.unit_group:  # движение юнитов
            unit.action(self.bot)

        for unit in self.bot.unit_group:  # движение вражеских юнитов
            unit.action(self.player)

        self.player.building_group.update()
        self.bot.building_group.update()

        draw_group = self.get_draw_group(self.player.building_group,
                                         self.bot.building_group,
                                         self.resource_group,
                                         self.player.unit_group,
                                         self.bot.unit_group)

        # отрисовка всех объекстов
        draw_group.draw(self.field)

        # обновление камеры
        self.client.update()
        self.camera.update(self.client)
        self.camera.apply(self.client)

        # отрисовка на экране
        field_pos = self.get_field_pos()
        self.screen.blit(self.field, (-field_pos[0], -field_pos[1]))

        # проверка наличия у каждого из игроков главных зданий
        return self.endgame_check()

    def check_resource(self, resource, unit):
        first_bool = self.resource_state % (constants.FPS * 2) == 0
        if first_bool is False:
            return False
        second_bool = resource.rect[0] - constants.MINING_AREA <= unit.rect[
            0] <= resource.rect[0] + constants.MINING_AREA
        if second_bool is False:
            return False
        third_bool = resource.rect[1] - constants.MINING_AREA <= unit.rect[
            1] <= resource.rect[1] + constants.MINING_AREA
        if third_bool is False:
            return False
        return True

    # сбор ресурсов
    def resource_update(self):
        from constants import WOOD_OUTPUT_SPEED, GOLD_OUTPUT_SPEED, \
            FOOD_OUTPUT_SPEED

        gathering_sprites = pygame.sprite.groupcollide(self.player.unit_group,
                                                       self.resource_group,
                                                       False, False)
        for resource in self.resource_group:
            for unit in gathering_sprites:
                if isinstance(unit, units.Settler):
                    if self.check_resource(resource, unit):
                        change_container = tuple()
                        if resource.get_type() == ResourceType.WOOD:
                            change_container = (0, WOOD_OUTPUT_SPEED, 0)
                        if resource.get_type() == ResourceType.GOLD:
                            change_container = (GOLD_OUTPUT_SPEED, 0, 0)
                        if resource.get_type() == ResourceType.FOOD:
                            change_container = (0, 0, FOOD_OUTPUT_SPEED)

                        self.player.resources.change_values(*change_container)

    # получение всех юнитов, видных на экране (их и нужно прорисовать)
    def get_draw_group(self, *groups):
        x_field_pos, y_field_pos = self.get_field_pos()
        field_rect = (x_field_pos, y_field_pos, self.field_window_width,
                      self.field_window_height)

        draw_group = pygame.sprite.Group()
        for group in groups:
            for group_object in group:
                if group_object.rect.colliderect(field_rect):
                    group_object.add(draw_group)

        return draw_group

    def get_field_pos(self):  # позиция поля относительно камеры
        return (self.client.rect.x, self.client.rect.y)

    def get_field_size(self):  # размер поля
        return self.field.get_size()

    # начало или окончание движения камеры в зависимости
    # от нажатой или отпущенной клавиши
    def change_player_directory(self, key, value):
        if key == pygame.K_LEFT:  # движения камеры
            self.client.left_dir = value
        elif key == pygame.K_RIGHT:
            self.client.right_dir = value
        elif key == pygame.K_UP:
            self.client.up_dir = value
        elif key == pygame.K_DOWN:
            self.client.down_dir = value

    # проверка наличия у каждого из игроков главных зданий
    def endgame_check(self):
        townhalls = self.player.townhalls.sprites()
        if len(townhalls) == 0:
            return GameState.PLAYER_LOSE
        townhalls = self.bot.townhalls.sprites()
        if len(townhalls) == 0:
            return GameState.PLAYER_WIN
        return GameState.GAME_CONTINUE
