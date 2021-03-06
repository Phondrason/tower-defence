import pygame as pg
from States import States
from MenuManager import MenuManager

class MainMenu(States, MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = ["game","continue"]
        self.options = ["Continue", "New Game", "Quit"]
        self.nextList = [["game", "continue"], ["newmenu", "none"]]
        self.preRenderOptions()
        self.spacer = 100
        self.fromBottom = 400 - (len(self.options) * self.spacer) / 2

    def cleanup(self):
        pass

    def startup(self, arg):
        pass

    def getEvent(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.getEventMenu(event)

    def update(self, screen):
        self.updateMenu()
        self.draw(screen)

    def draw(self, screen):
        screen.fill((20,20,20))
        self.drawMenu(screen)
