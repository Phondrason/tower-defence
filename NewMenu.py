import pygame as pg
from States import States
from MenuManager import MenuManager

class NewMenu(States, MenuManager):
    def __init__(self, screensize=[900,800]):
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = ["menu","none"]
        self.options = ["Yes", "No"]
        self.nextList = [["game","new"], ["menu","none"]]
        self.preRenderOptions()
        self.spacer = 100
        self.fromBottom = screensize[1] / 2 - (len(self.options) * self.spacer) / 2
        
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