import pygame
import constants


def game_ending(screen, width, height, text="You won!!!"):
    surface_size = (width // 4.8, height // 5.4)
    surface = pygame.Surface((surface_size[0], surface_size[1]))
    surface.fill(constants.GREY)

    text_ending = pygame.font.SysFont('Calibri', width // 27)
    text = text_ending.render(text, True, constants.BLACK)
    surface_pos = ((width - surface_size[0]) // 2,
                   (height - surface_size[1]) // 2)
    surface.blit(text, (surface_size[0] // 2 - width // 12.8,
                        surface_size[1] // 2 - 30))
    screen.blit(surface, surface_pos)

    while True:
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    exit()

        pygame.display.update()
