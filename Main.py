import pygame, sys, UI
from pygame.locals import *

pygame.init()
display = pygame.display.set_mode((640,480))
pygame.display.set_caption("Network Science Fair")
buttons = []
buttons.append(UI.MenuButton(display.get_rect().center, 300, 90, "test"))
while True:
    display.fill((255, 255, 255))
    for button in buttons:
        display.blit(button.surface, button.position)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            for button in buttons:
                button.event(event.pos)
            print(event.button, " @ coord ", event.pos)
    pygame.display.update()
