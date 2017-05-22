import pygame, sys, UI, Screen
from pygame.locals import *

class ScienceFair:
    
    #setups up pygame window
    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Network Science Fair")
        test = UI.CenteredText(200, "Hello this is a test and I hope it works")
        [print(x) for x in test.lines]
    #puts up main menu and starts main game loop
    def start(self):
        UI.Drawable.game = self
        self.screen = Screen.MainMenu()
        #uses a double buffer for drawing and polls events
        while True:
            self.screen.drawScreen()
            self.pollEvents()
            pygame.display.update()

    #searches through the event que for mouse clicks or the exit command
    def pollEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                for button in self.screen.buttons:
                    button.event(event.pos)
                print(event.button, " @ coord ", event.pos)
    #allows buttons to change the current screen of the window
    def changeScreen(self, newScreen):
        self.screen = newScreen
#actually makes instanceof ScienceFair and runs it
if __name__ == "__main__":
    game = ScienceFair(400,600)
    game.start()
