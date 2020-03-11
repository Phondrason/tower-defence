import pygame as pg
from States import States
from Vector import Vector
from Turret import Turret
from Enemy import Enemy
from Projectile import Projectile
from Button import Button
import json, os

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = ["menu", "none"]
        self.boardSurface = pg.Surface((800, 600), pg.SRCALPHA)
        self.boardRect = self.boardSurface.get_rect()
        self.boardRect.topleft = [50, 150]
        self.sellButton = Button((600, 60), (90, 30), "Sell", centery=True)
        self.upgradeButton = Button((600, 110), (90, 30), "Upgrade", centery=True)
        self.skipButton = Button((175, 775), (80, 30), "Skip", centery=True)
        self.skipButton.visible = True
        self.projectiles = []
        self.loadMedia()
        self.newGame()
    
    def loadMedia(self):
        self.fonts = {
            "50": pg.font.SysFont("Calibri", 50),
            "20": pg.font.SysFont("Calibri", 20)
        }
        self.images = {
            "coin": pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\\images\\coin.png").convert_alpha(), (44, 44)),
            "heart": pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\\images\\heart.png").convert_alpha(), (45, 39)),
            "hourglass": pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\\images\\hourglass.png").convert_alpha(), (22, 40))
        }
    
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
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.boardRect.collidepoint(event.pos):
                self.click(Vector(event.pos) - Vector(self.boardRect.topleft))
            elif self.sellButton.rect.collidepoint(event.pos) and self.sellButton.enabled:
                self.money += self.selected.cost // 0.6
                self.selected.selected = False
                self.turrets.remove(self.selected)
                x, y = self.selected.pos
                self.matrix[y][x] = "empty"
                self.selected = None
                self.sellButton.enabled = False
                self.sellButton.visible = False
                self.upgradeButton.visible = False
                self.upgradeButton.enabled = False
            elif self.upgradeButton.rect.collidepoint(event.pos) and self.upgradeButton.enabled:
                if self.money >= self.selected.upgradeCost:
                    self.money -= self.selected.upgradeCost
                    self.selected.upgrade()
            elif self.skipButton.rect.collidepoint(event.pos) and self.skipButton.enabled:
                self.spawnWave()
                self.skipButton.enabled = False
                

    def update(self, screen):
        self.spawnTimer -= 1
        for enemy in self.enemies:
            if enemy.move():
                self.health -= 10
                self.enemies.remove(enemy)
                enemy.selected = False
        self.attack()
        for projectile in self.projectiles:
            if projectile.update():
                self.projectiles.remove(projectile)
        if self.selected is not None and type(self.selected).__name__ == "Turret":
            self.upgradeButton.enabled = self.money >= self.selected.upgradeCost
        else:
            self.upgradeButton.enabled = False
        if len(self.enemies) == 0:
            self.skipButton.enabled = True
        if self.spawnTimer == 0:
            self.spawnWave()
        self.draw(screen)
    
    def attack(self):
        for turret in self.turrets:
            turret.cooldown -= 1
            if turret.cooldown <= 0:
                eligible = [enemy for enemy in self.enemies if (Vector(enemy.rect.center) - Vector(turret.rect.center)).norm() <= turret.range]
                if len(eligible) > 0:
                    target = min(eligible, key=lambda enemy: len(enemy.waypoints))
                    self.projectiles.append(Projectile(turret, target))
                    if turret.attack(target) <= 0:
                        self.money += target.value
                        self.enemies.remove(target)
                        if target.selected:
                            self.selected = None
    
    def draw(self, screen):
        screen.fill((20,20,20))
        self.drawBoard(screen)
        self.renderImage(screen, self.images["hourglass"], (50, 775), False, True)
        self.renderText(screen, round(self.spawnTimer / 60, 1), 50, (75, 775), False, True)
        self.renderImage(screen, self.images["coin"], (50, 125), False, True)
        self.renderText(screen, self.money, 50, (100, 125), False, True)
        self.renderImage(screen, self.images["heart"], (750, 775), False, True)
        self.renderText(screen, self.health, 50, (800, 775), False, True)
        if self.sellButton.visible: self.sellButton.draw(screen)
        if self.upgradeButton.visible: self.upgradeButton.draw(screen)
        self.skipButton.draw(screen)
        if self.selected is not None:
            i = 1
            self.renderText(screen, type(self.selected).__name__, 20, (700, 30), centery=True)
            pg.draw.line(screen, (255,255,255), (700, 40), (800, 40))
            for row in self.selected.getStats():
                self.renderText(screen, row, 20, (700, 35+i*20), centery=True)
                i += 1
    
    def drawBoard(self, screen):
        self.boardSurface.fill((70,155,30))
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == "path": pg.draw.rect(self.boardSurface, (214,148,27), (x*40, y*40, 40, 40))
        for enemy in self.enemies:
            enemy.draw(self.boardSurface)
        for turret in self.turrets:
            turret.draw(self.boardSurface)
        for projectile in self.projectiles:
            projectile.draw(self.boardSurface)
        screen.blit(self.boardSurface, self.boardRect)
        
    def renderImage(self, screen, image, pos, centerx=False, centery=False):
        width, height = image.get_size()
        posx, posy = pos
        if centerx:
            posx = pos[0] - width // 2
        if centery:
            posy = pos[1] - height // 2
        screen.blit(image, (posx, posy))
        
    def renderText(self, screen, text, size, pos, centerx=False, centery=False):
        #centerx & centery = centers text on given position
        render = self.fonts[str(size)].render(str(text), True, (255,255,255))
        self.renderImage(screen, render, pos, centerx, centery)
    
    def newGame(self):
        self.matrix = [["empty" for x in range(20)] for y in range(15)]
        self.waypoints = [[1,0],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[18,2],[18,3],[17,3],[16,3],[15,3],[14,3],[13,3],[12,3],[11,3],[10,3],[9,3],[8,3],[7,3],[6,3],[5,3],[4,3],[3,3],[2,3],[1,3],[1,4],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],[9,5],[10,5],[11,5],[12,5],[13,5],[14,5],[15,5],[16,5],[17,5],[18,5],[18,6],[18,7],[17,7],[16,7],[15,7],[14,7],[13,7],[12,7],[11,7],[10,7],[9,7],[8,7],[7,7],[6,7],[5,7],[4,7],[3,7],[2,7],[1,7],[1,8],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],[10,9],[11,9],[12,9],[13,9],[14,9],[15,9],[16,9],[17,9],[18,9],[18,10],[18,11],[17,11],[16,11],[15,11],[14,11],[13,11],[12,11],[11,11],[10,11],[9,11],[8,11],[7,11],[6,11],[5,11],[4,11],[3,11],[2,11],[1,11],[1,12],[1,13],[2,13],[3,13],[4,13],[5,13],[6,13],[7,13],[8,13],[9,13],[10,13],[11,13],[12,13],[13,13],[14,13],[15,13],[16,13],[17,13],[18,13],[18,14]]
        for x, y in self.waypoints: 
            self.matrix[y][x] = "path"
            pg.draw.rect(self.boardSurface, (214,148,27), (x*40, y*40, 40, 40))
        self.enemies = []
        self.spawnWave()
        self.money = 200
        self.health = 100
        self.turrets = []
        self.selected = None

    def saveGame(self):
        dict = {
            "matrix": self.matrix,
            "turrets": [turret.save() for turret in self.turrets],
            "enemies": [enemy.save() for enemy in self.enemies],
            "spawnTimer": self.spawnTimer,
            "money": self.money,
            "health": self.health
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
                self.health = dict["health"]
        except:
            self.newGame()
            
    def spawnWave(self):
        self.enemies.extend([Enemy(Vector(40, -40*i), self.waypoints[:], health=100, totalhealth=100, speed=2) for i in range(1, 11)])
        self.spawnTimer = 1800
        self.skipButton.enabled = False

    def click(self, pos):
        x, y = pos // 40
        if self.selected is not None:
            self.selected.selected = False
        if self.matrix[y][x] == "empty" and self.money >= 100:
            self.money -= 100
            self.matrix[y][x] = "turret"
            new = Turret(pos // 40)
            self.turrets.append(new)
            
        for turret in self.turrets:
            if turret.rect.collidepoint(pos):
                turret.selected = True
                self.selected = turret
                self.sellButton.enabled = True
                self.upgradeButton.enabled = False
                self.sellButton.visible = True
                self.upgradeButton.visible = True
                return
                
        for enemy in self.enemies:
            if enemy.rect.collidepoint(pos):
                enemy.selected = True
                self.selected = enemy
                self.sellButton.enabled = False
                self.upgradeButton.enabled = False
                self.sellButton.visible = False
                self.upgradeButton.visible = False
                return
        self.selected = None
        self.sellButton.enabled = False
        self.upgradeButton.enabled = False
        self.sellButton.visible = False
        self.upgradeButton.visible = False