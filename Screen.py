import pygame, abc, UI
from pygame.locals import *
from UI import *


"""
Screen MUST be instantiated after the pygame display
"""

class Screen:    
    def __init__(self,backgroundPath):
        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()
        
        #Used for double buffering to avoid any flickering when drawing too many objects
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.convert()
        #declares the list of the drawables and buttons in order to keep them unique to each Screen obj
        self.drawables = []
        self.buttons = []
        self.drawables.append(UI.Drawable((0,0), width, height,False, backgroundPath))                

                                                  
    def addButton(self, button):
        self.drawables.append(button)
        self.buttons.append(button)
        
    def drawScreen(self):
        for x in self.drawables:
            self.surface.blit(x.surface, x.position)
        pygame.display.get_surface().blit(self.surface, (0,0))

class MainMenu(Screen):
    def __init__(self):
        Screen.__init__(self, "menu.png")
        #Add MenuButtons
        xCenter = self.surface.get_rect().centerx
        PlayGameButton = UI.MenuButton((xCenter, 200), 200,100, "Play", "Game")
        self.addButton(PlayGameButton)
class Game(Screen):
    def __init__(self):
        Screen.__init__(self, "menu.png")
        for x in self.buttons:
            print(x)
        
