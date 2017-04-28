import pygame, abc
from abc import ABC, ABCMeta
from pygame.locals import *

class Drawable(ABC):
    def __init__(self, position, width, height, imagePath):
        #init vars
        self.x = position[0] - int(width/2)
        self.y = position[1] - int(height/2)
        self.position = (self.x, self.y)
        self.width = width
        self.height = height

        #create surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        #speeds up drawing
        self.surface.convert()
        self.surface.blit(pygame.transform.scale(pygame.image.load(imagePath), (width, height)), (0,0))

class Button(Drawable):
    @abc.abstractmethod
    def __init__(self, position, width, height, text):
        super().__init__(position, width, height, "Button.png")
        #makes this abstract
        __metaclass__ = ABCMeta
                
        #drawing to the text
        self.text = text
        font = pygame.font.Font("freesansbold.ttf", 32)
        txtColor = (150,150,150)
        self.surface.blit(font.render(text, True,txtColor), (13,8))

    def event(self, coord):
        print("add proper exception here soon")
class MenuButton(Button):
    def __init__(self, position, width, height, text):
        super().__init__(position, width, height, text)

    def event(self, coord):
        if self.surface.get_rect().collidepoint(coord[0]-self.x, coord[1]-self.y):
            print("button pressed")
        
