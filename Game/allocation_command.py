import pygame
import constants
import squad
from command import Command


# выделение юнитов на поле
class AllocationCommand(Command):
    def event(self, button_key):
        if button_key is not None:
            return
        x_pos, y_pos = pygame.mouse.get_pos()
        rect = None
        while pygame.mouse.get_pressed()[0] == 1:  # пока нажата кнопка мыши...
            for j in pygame.event.get():
                if j.type == pygame.KEYUP:
                    self.world.change_player_directory(j.key, False)
                elif j.type == pygame.KEYDOWN:
                    self.world.change_player_directory(j.key, True)

                self.world.update()

                # создание области выделения юнитов
                field_pos = self.world.get_field_pos()
                rect_pos = [x_pos + field_pos[0], y_pos + field_pos[1],
                            pygame.mouse.get_pos()[0] - x_pos,
                            pygame.mouse.get_pos()[1] - y_pos]
                rect = pygame.draw.rect(self.world.field, constants.BLUE,
                                        rect_pos, 3)

                self.world.screen.blit(self.world.field,
                                       (-field_pos[0], -field_pos[1]))
                self.menu.blit(self.world.screen)
                pygame.display.update()

        # создание нового отряда из юнитов
        self.world.new_army = squad.Army()
        for unit in self.world.player.unit_group:
            if rect.colliderect(unit.rect):
                self.world.new_army.add(unit)
