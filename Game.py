import pygame as pg
from States import States
from Vector import Vector
from Turret import Turret
from Enemy import Enemy
import json, os

class Game(States):
    def __init__(self, screensize=[900,800]):
        States.__init__(self)
        self.next = ["menu", "none"]
        self.boardSurface = pg.Surface((800, 600), pg.SRCALPHA)
        self.boardRect = self.boardSurface.get_rect()
        self.boardRect.bottomleft = [50, screensize[1]-50]
        self.font = pg.font.SysFont("Calibri", 50)
        self.newGame()

    def cleanup(self):
        self.saveGame()

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
                self.click(Vector(event.pos) - Vector(self.boardRect.topleft))
                
    def update(self, screen):
        self.spawnTimer -= 1
        for enemy in self.enemies:
            if enemy.move():
                print("rip")
        self.attack()
        if len(self.enemies) == 0 or self.spawnTimer == 0:
            self.enemies.extend(self.spawnWave())
            self.spawnTimer = 1800
        self.draw(screen)
    
    def attack(self):
        for turret in self.turrets:
            turret.cooldown -= 1
            if turret.cooldown <= 0:
                eligible = [enemy for enemy in self.enemies if (Vector(enemy.rect.center) - Vector(turret.rect.center)).norm() <= turret.range]
                if len(eligible) > 0:
                    target = min(eligible, key=lambda enemy: len(enemy.waypoints))
                    if turret.attack(target) < 0:
                        self.money += target.value
                        self.enemies.remove(target)
    
    def draw(self, screen):
        screen.fill((20,20,20))
        self.boardSurface.fill((70,155,30))
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == "path": pg.draw.rect(self.boardSurface, (214,148,27), (x*40, y*40, 40, 40))
        for enemy in self.enemies:
            enemy.draw(self.boardSurface)
        for turret in self.turrets:
            turret.draw(self.boardSurface)
        timer = self.font.render(str(round(self.spawnTimer / 60, 1)), True, (255,255,255))
        money = self.font.render(str(self.money), True, (255,255,255))
        self.screen.blit(timer, (50, 100))
        self.screen.blit(money, (200,100))
        screen.blit(self.boardSurface, self.boardRect)
        
    def newGame(self):
        self.matrix = [["empty" for x in range(20)] for y in range(15)]
        self.waypoints = [[1,0],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[18,2],[18,3],[17,3],[16,3],[15,3],[14,3],[13,3],[12,3],[11,3],[10,3],[9,3],[8,3],[7,3],[6,3],[5,3],[4,3],[3,3],[2,3],[1,3],[1,4],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],[9,5],[10,5],[11,5],[12,5],[13,5],[14,5],[15,5],[16,5],[17,5],[18,5],[18,6],[18,7],[17,7],[16,7],[15,7],[14,7],[13,7],[12,7],[11,7],[10,7],[9,7],[8,7],[7,7],[6,7],[5,7],[4,7],[3,7],[2,7],[1,7],[1,8],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],[10,9],[11,9],[12,9],[13,9],[14,9],[15,9],[16,9],[17,9],[18,9],[18,10],[18,11],[17,11],[16,11],[15,11],[14,11],[13,11],[12,11],[11,11],[10,11],[9,11],[8,11],[7,11],[6,11],[5,11],[4,11],[3,11],[2,11],[1,11],[1,12],[1,13],[2,13],[3,13],[4,13],[5,13],[6,13],[7,13],[8,13],[9,13],[10,13],[11,13],[12,13],[13,13],[14,13],[15,13],[16,13],[17,13],[18,13],[18,14]]
        for x, y in self.waypoints: 
            self.matrix[y][x] = "path"
            pg.draw.rect(self.boardSurface, (214,148,27), (x*40, y*40, 40, 40))
        self.enemies = self.spawnWave()
        self.spawnTimer = 1800
        self.money = 200
        self.turrets = []
        self.selected = None

    def saveGame(self):
        dict = {
            "matrix": self.matrix,
            "turrets": [turret.save() for turret in self.turrets],
            "enemies": [enemy.save() for enemy in self.enemies],
            "spawnTimer": self.spawnTimer,
            "money": self.money
        }
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\saves\\savefile.json","w") as f:
            json.dump(dict, f)

    def loadGame(self):
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + "\\saves\\savefile.json","r") as f:
                dict = json.load(f)
                self.matrix = dict["matrix"]
                self.turrets = [Turret(Vector(turret["position"]), turret["damage"], turret["range"], turret["attackspeed"], turret["cost"], turret["cooldown"]) for turret in dict["turrets"]]
                self.enemies = [Enemy(Vector(enemy["position"]), enemy["waypoints"], Vector(enemy["next"]), enemy["health"], enemy["totalhealth"], enemy["speed"], enemy["value"]) for enemy in dict["enemies"]]
                self.spawnTimer = dict["spawnTimer"]
                self.money = dict["money"]
        except:
            self.newGame()
            
    def spawnWave(self):
        return [Enemy(Vector(40, -40*i), self.waypoints[:], health=100, totalhealth=100, speed=2) for i in range(1, 11)]

    def click(self, pos):
        x, y = pos // 40
        if self.selected is not None:
            self.selected.selected = False
        if self.matrix[y][x] == "empty" and self.money >= 100:
            self.money -= 100
            self.matrix[y][x] = "turret"
            new = Turret(pos // 40)
            new.selected = True
            self.selected = new
            self.turrets.append(new)
        elif self.matrix[y][x] == "turret":
            for turret in self.turrets:
                if turret.rect.collidepoint(pos):
                    turret.selected = True
                    self.selected = turret