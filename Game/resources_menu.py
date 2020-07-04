import pygame
from resources import Resources
from block import Block
from resources_events import ResourceEvent


class ResourcesMenu:  # информационное меню
    def __init__(self, field_width, resources):
        resources_num = 3
        self.menu_blocks = []
        indent = field_width // (8 * (resources_num + 1))
        block_width = (field_width -
                       indent * (resources_num + 1)) // resources_num
        block_height = pygame.display.get_surface().get_size()[1] // 18

        resources_names = Resources.get_resources_names()
        event_types = list(ResourceEvent)
        current_pos = indent
        for i in range(resources_num):
            new_block = Block(block_width, block_height, current_pos,
                              resources_names[i])
            self.menu_blocks.append(new_block)
            resources.manager.subscribe(event_types[i], new_block)
            current_pos += indent + block_width
        resources.change_values(0, 0, 0)

    def blit(self, surface: pygame.Surface):
        for i in range(len(self.menu_blocks)):
            surface.blit(self.menu_blocks[i].surface,
                         (self.menu_blocks[i].x_pos, 0))
