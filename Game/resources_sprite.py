import os
import pygame
import constants
from help_structures import ObjectCollision


class ResourcesSprite(pygame.sprite.Sprite):
    def __init__(self, group, image, pos, size, res_type):
        super().__init__()
        image_name = os.path.join(os.getcwd(), 'resources_images', image)
        self.image = pygame.image.load(image_name)
        self.image.set_colorkey(constants.TRANSPARENT)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=pos)

        for obj in group:
            if pygame.sprite.collide_rect(self, obj):
                raise ObjectCollision

        self.resource_type = res_type
        self.add(group)

    def get_type(self):
        return self.resource_type
