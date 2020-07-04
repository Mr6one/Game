import pygame
import constants
from world import World
from menu import Menu
from help_structures import GameState
from field_command import FieldCommand
from menu_command import MenuCommand
from keydown_command import KeyDownCommand
from keyup_command import KeyUpCommand
from allocation_command import AllocationCommand
from unit_menu_command import UnitMenuCommand
from game_ending import game_ending


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # создание окна приложения
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Game")
    width, height = pygame.display.get_surface().get_size()
    picture_sz = height // 6

    # генерация мира
    world = World(width - picture_sz, screen)
    screen.blit(world.field, (0, 0))

    # массив названий зданий
    buildings_names = ['barrack', 'castle', 'townhall', 'stable', 'market',
                       'archery_range', 'tower', 'farm']

    # создание боковой панели
    menu = Menu(picture_sz, [world.field_window_width, 0], buildings_names,
                world.player.resources)
    menu.blit(screen)

    # инициализация команд
    field_command = FieldCommand(world, menu)
    menu_command = MenuCommand(world, menu)
    keydown_command = KeyDownCommand(world, menu)
    keyup_command = KeyUpCommand(world, menu)
    allocation_command = AllocationCommand(world, menu)
    unit_menu_command = UnitMenuCommand(world, menu)

    pygame.display.update()

    while True:  # mainloop
        for i in pygame.event.get():  # обработка событий
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    exit()
                keydown_command.event(i.key)
            elif i.type == pygame.KEYUP:
                keyup_command.event(i.key)
            elif i.type == pygame.MOUSEBUTTONDOWN:  # события мыши
                mouse_pos = pygame.mouse.get_pos()

                menu.current_state_update()
                # если курсор на боковой панели
                if mouse_pos[0] > world.field_window_width:
                    menu_command.event(i.button)
                elif menu.check_mouse_pos_on_unit_menu(mouse_pos):
                    unit_menu_command.event(i.button)
                else:  # если курсор на основном поле
                    field_command.event(i.button)
            elif i.type == pygame.MOUSEMOTION and \
                    pygame.mouse.get_pressed()[0] == 1:
                allocation_command.event(None)

        endgame = world.update()
        menu.blit(screen)

        if endgame == GameState.PLAYER_WIN:
            game_ending(screen, width, height, "You won!!!")
        elif endgame == GameState.PLAYER_LOSE:
            game_ending(screen, width, height, "You lost(((")

        pygame.display.update()
        clock.tick(constants.FPS)


if __name__ == "__main__":
    main()
