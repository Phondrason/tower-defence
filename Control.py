import pygame as pg

class Control():
    def __init__(self, SCREENSIZE=[900,800]):
        self.screen = pg.display.set_mode(SCREENSIZE)
        self.screenRect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False

    def setupStates(self, stateDict, startState):
        self.stateDict = stateDict
        self.stateName = startState
        self.state = self.stateDict[self.stateName]
    
    def switchStates(self):
        self.state.done = False
        previous = self.stateName
        self.stateName, arg = self.state.next
        self.state.cleanup()
        self.state = self.stateDict[self.stateName]
        self.state.startup(arg)
        self.state.previous = previous
    
    def eventLoop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.getEvent(event)

    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.switchStates()
        self.state.update(self.screen)

    def mainLoop(self):
        while not self.done:
            self.clock.tick(self.fps)
            self.eventLoop()
            self.update()
            pg.display.update()
