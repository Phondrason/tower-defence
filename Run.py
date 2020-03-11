from MainMenu import MainMenu
from NewMenu import NewMenu
from Game import Game
from Control import Control
import pygame as pg

if __name__ == "__main__":
    pg.init()
    app = Control()
    stateDict =  {
        "menu": MainMenu(),
        "game": Game(),
        "newmenu": NewMenu()
    }
    app.setupStates(stateDict, "menu")
    app.mainLoop()
    pg.quit()
