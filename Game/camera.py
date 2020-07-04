import pygame


class Camera(object):
    def __init__(self, camera_func, width, height, size):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        self.field_width = size[0]
        self.field_height = size[1]

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect,
                                      self.field_width, self.field_height)


def camera_configure(camera, target_rect, field_width, field_height):
    current_x, current_y, _, _ = target_rect
    _, _, width, height = camera
    current_x = -current_x + field_width / 2
    current_y = -current_y + field_height / 2

    current_x = min(0, current_x)
    current_x = max(-(camera.width - field_width), current_x)
    current_y = max(-(camera.height - field_height), current_y)
    current_y = min(0, current_y)

    return pygame.Rect(current_x, current_y, width, height)


class Client(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, max_pos_x, max_pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.left_dir = False
        self.right_dir = False
        self.up_dir = False
        self.down_dir = False
        self.xvel = 0
        self.yvel = 0
        self.speed = 10
        self.rect = pygame.Rect(x_pos, y_pos, 10, 10)
        self.max_pos_x = max_pos_x
        self.max_pos_y = max_pos_y

    def update(self):
        if self.left_dir:
            self.xvel = -self.speed

        if self.right_dir:
            self.xvel = self.speed

        if self.up_dir:
            self.yvel = -self.speed

        if self.down_dir:
            self.yvel = self.speed

        if not (self.left_dir or self.right_dir):
            self.xvel = 0

        if not (self.up_dir or self.down_dir):
            self.yvel = 0

        self.rect.x += self.xvel
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > self.max_pos_x:
            self.rect.x = self.max_pos_x
        self.rect.y += self.yvel
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > self.max_pos_y:
            self.rect.y = self.max_pos_y
