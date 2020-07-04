from gui import *
import pygame
import random


#проверка того, что все юниты достигли своих целей
def goal_achievement_test():
    unit_group = pygame.sprite.Group()
    unit_list = [ArcherCreator(), ArbalesterCreator(), SwordsmanCreator(), SpearCreator()]
    test_res = True
    max_width = max_height = 4000

    for i in range(1000):
        unit_type: UnitCreator = unit_list[random.randint(0, 3)]
        try:
            unit = unit_type.create_unit((random.randint(0, max_width), random.randint(0, max_height)), unit_group)
        except ObjectCollision:
            pass
        goal_pos = (random.randint(0, max_width), random.randint(0, max_height))
        unit.set_goal(goal_pos)

        while True:
            unit.move()
            if unit.direction == Direction.NONE:
                break
        if goal_pos[0] - 2 <= unit.rect.center[0] <= goal_pos[0] + 2 and \
                goal_pos[1] - 2 <= unit.rect.center[1] <= goal_pos[1] + 2 \
                and unit.rect.center[1] >= goal_pos[1] - 2:
            print('OK')
        else:
            test_res = False
            print('FAIL')
    if test_res:
        print('\neverything is OK')
    else:
        raise ValueError


#проверка того, что создалось именно то здание, которое выбрал пользователь
def check_building_creation():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()
    picture_sz = height // 6

    buildings = ['barrack', 'castle', 'townhall', 'stable', 'market', 'archeryrange', 'tower', 'farm']
    world = World(width - picture_sz)
    menu = Menu(picture_sz, [world.field_window_width, 0], buildings)

    test_res = True
    for i in range(100):
        menu_mouse_pos = (random.randint(width-picture_sz, width), random.randint(0, height))
        field_mouse_pos = (random.randint(0, width-picture_sz-1), random.randint(0, height))
        selected_building = int(selected_building_num(menu_mouse_pos, menu.pos, menu.picture_sz))
        world.selected_building = selected_building
        try:
            created_building = building_creation(buildings, world, field_mouse_pos) #созданное пользователем здание
            if buildings[selected_building] == str(created_building).lower()[1:len(str(buildings[selected_building]))+1]:
                print('OK')
            else:
                test_res = False
                print('FAIL')
        except ObjectCollision:
            pass

    if test_res:
        print('\neverything is OK')
    else:
        raise ValueError


#проверка того, что создался именно тот юнит, которого выбрал пользователь
def check_unit_creation():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    buildings = [Barrack, ArcheryRange]
    unit_types = [[UnitType.SPEAR, UnitType.SWORDSMAN], [UnitType.ARCHER, UnitType.ARBALESTER]]
    unit_group = pygame.sprite.Group()
    building_group = pygame.sprite.Group()
    max_width = max_height = 4000

    test_res = True
    for i in range(1000):
        selected_building = random.randint(0, 1)
        try:
            building = buildings[selected_building]((random.randint(0, max_width), random.randint(0, max_height)),
                                                    building_group)
            selected_unit = random.randint(0, 1)
            unit = create_unit_from_building(building, unit_group, unit_types[selected_building][selected_unit])
            initial_unit = str(unit_types[selected_building][selected_unit]).lower()[9:]
            if str(unit)[1:len(initial_unit)+1].lower() == initial_unit:
                print('OK')
            else:
                print('FAIL')
                test_res = False
        except ObjectCollision:
            pass

    if test_res:
        print('\neverything is OK')
    else:
        raise ValueError


goal_achievement_test()
check_building_creation()
check_unit_creation()
