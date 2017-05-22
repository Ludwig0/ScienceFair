import pygame, abc, ScienceFair ,Screen
from abc import ABC, ABCMeta
from pygame.locals import *

class Drawable:
    game = None
    def __init__(self, position, width, height, centered,imagePath):
        #init vars
        if centered:
            self.x = position[0] - width/2
            self.y = position[1] - height/2
        else:
            self.x = position[0]
            self.y = position[1]
        self.position = (self.x, self.y)
        self.width = width
        self.height = height

        #create surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        #speeds up drawing
        self.surface.convert()
        self.surface.blit(pygame.transform.scale(pygame.image.load(imagePath), (width, height)), (0,0))        

class Button(Drawable):
    """
    *Creates a button in at a given position with a given size
    *Button has the text passed in written on it (centered)
    """
    @abc.abstractmethod
    def __init__(self, position, width, height, text):
        #Necessary to make the class abstract
        __metaclass__ = abc.ABCMeta
        #setups the drawable parent so everything related to drawing is handled now
        super().__init__(position, width, height, True, "Button.png")

              
        #drawing to the text
        #TODO// MAKE A TEXT CLASS
        self.text = text
        font = pygame.font.Font("freesansbold.ttf", 32)
        txtColor = (150,150,150)
        self.surface.blit(font.render(text, True,txtColor), (13,8))

    def event(self, coord):
        if self.surface.get_rect().collidepoint(coord[0]-self.x, coord[1]-self.y):
            self.eventAction()
    @abc.abstractmethod
    def eventAction(self):
        pass
    
class MenuButton(Button):
    def __init__(self, position, width, height, text, destination):
        super().__init__(position, width, height, text)
        self.destination = destination
    def eventAction(self):
        newScreen = {
            "MainMenu":Screen.MainMenu(),
            "Game":Screen.Game()
            }[self.destination]
        Drawable.game.changeScreen(newScreen)
class CenteredText:
    #position is top right, width is the distance the text goes before wrapping
    def __init__(self, width, text):
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.lines = []
        line = []
        for char in text:
            line.append(char)
            currentLineSize = self.font.size("".join([x for x in line]))
            if currentLineSize[0] > width:
                self.lines.append("".join([x for x in line[:len(line)-1]]))
                line = line[len(line)-1:]
