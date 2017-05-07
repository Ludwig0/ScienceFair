import pygame, abc, UI
from pygame.locals import *
from UI import *


class Screen:
    drawables = []
    buttons = []
    def __init__(self, width, height, backgroundPath):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.convert()
        self.drawables.append(Drawable((0,0), width, height,False, backgroundPath))                
                         
    def addButton(self, position, width, height, text):
        button = UI.MenuButton(position, width, height, text)
        self.drawables.append(button)
        self.buttons.append(button)
        
    def drawScreen(self):
        for x in self.drawables:
            self.surface.blit(x.surface, x.position)

class MainMenu(Screen):
    def __init__(self, width, height):
        Screen.__init__(self,width, height, "menu.png")
        self.addButton(self.surface.get_rect().center, 200, 50, "test")        
            
