from MainMenu import MainMenu
from NewMenu import NewMenu
from Game import Game
from Control import Control
import pygame as pg

if __name__ == "__main__":
    SCREENSIZE = [900, 800]
    pg.init()
    app = Control(SCREENSIZE)
    stateDict =  {
        "menu": MainMenu(SCREENSIZE),
        "game": Game(SCREENSIZE),
        "newmenu": NewMenu(SCREENSIZE)
    }
    app.setupStates(stateDict, "menu")
    app.mainLoop()
    pg.quit()
