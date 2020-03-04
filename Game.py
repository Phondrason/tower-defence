import pygame as pg
from States import States
from Board import Board
from Enemy import Enemy
from Vector import Vector
from Turret import Turret
import json, os

class Game(States):
    def __init__(self, screensize=[900,800]):
        States.__init__(self)
        self.next = ["menu", "none"]
        self.boardSurface = pg.Surface((800, 600), pg.SRCALPHA)
        self.boardRect = self.boardSurface.get_rect()
        self.boardRect.bottomleft = [50, screensize[1]-50]
        self.newGame()

    def cleanup(self):
        self.saveGame()

    def saveGame(self):
        saveDict = {
            "boardMatrix": self.board.matrix,
            "turrets": [turret.save() for turret in self.board.turrets],
            "enemies": [enemy.save() for enemy in self.enemies]
        }
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\saves\\savefile.json","w") as f:
            json.dump(saveDict, f)

    def newGame(self):
        self.board = Board()
        self.enemies = [Enemy(Vector(40, 40*i), self.board.waypoints[:]) for i in range(-1, -11, -1)]

    def loadGame(self):
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + "\\saves\\savefile.json","r") as f:
                saveDict = json.load(f)
                self.board = Board()
                self.board.matrix = saveDict["boardMatrix"]
                self.board.turrets = [Turret(Vector(turret["position"]), turret["damage"], turret["range"], turret["attackspeed"], turret["cost"]) for turret in saveDict["turrets"]]
                self.enemies = [Enemy(Vector(enemy["position"]), enemy["waypoints"], Vector(enemy["next"]), enemy["health"], enemy["speed"]) for enemy in saveDict["enemies"]]
        except:
            self.newGame()

    def startup(self, arg):
        if arg == "new":
            self.newGame()
        elif arg == "continue":
            self.loadGame()
        else:
            self.done = True

    def getEvent(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.boardRect.collidepoint(event.pos):
                self.board.click(Vector(event.pos) - Vector(self.boardRect.topleft))

    def update(self, screen):
        for enemy in self.enemies:
            if enemy.move():
                self.done = True
        self.draw(screen)

    def draw(self, screen):
        screen.fill((20,20,20))
        self.board.draw(self.boardSurface)
        for enemy in self.enemies:
            enemy.draw(self.boardSurface)
        screen.blit(self.boardSurface, self.boardRect)