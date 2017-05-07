import pygame, sys, UI, Screen
from pygame.locals import *

WIDTH = 400
HEIGHT = 600

pygame.init()
display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Network Science Fair")
currentScreen = Screen.MainMenu(WIDTH, HEIGHT)

while True:
    currentScreen.drawScreen()
    display.blit(currentScreen.surface, (0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            for button in currentScreen.buttons:
                button.event(event.pos)
            print(event.button, " @ coord ", event.pos)
    pygame.display.update()
