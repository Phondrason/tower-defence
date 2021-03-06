import pygame as pg
from Vector import Vector

class Turret():
    def __init__(self, matrixpos, damage=20, range=200, attackspeed=2.0, cost=100, cooldown=0):
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = matrixpos * 40
        pg.draw.circle(self.image, (200,200,0), [20, 20], 15)
        self.pos = Vector(matrixpos)
        self.damage = damage
        self.range = range
        self.attackspeed = attackspeed
        self.cost = cost
        self.upgradeCost = cost // 2
        self.cooldown = cooldown
        self.selected = False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.selected:
            pg.draw.circle(screen, (255,255,255), self.rect.center, self.range, 2)
            
    def getStats(self):
        return ["Damage: {}".format(self.damage), "Range: {}".format(self.range), "Attackpeed: {}".format(self.attackspeed), "Value: {}".format(self.cost), "Upgradecost: {}".format(self.upgradeCost)]
    
    def upgrade(self):
        self.cost += self.upgradeCost
        self.upgradeCost = self.cost // 2
        self.damage += self.damage // 5
        self.range += self.range // 5
        self.attackspeed += round(self.attackspeed / 5, 1)
    
    def save(self):
        return {
            "position": self.pos.serialize(),
            "damage": self.damage,
            "range": self.range,
            "attackspeed": self.attackspeed,
            "cost": self.cost,
            "cooldown": self.cooldown
        }
    
    def attack(self, target):
        target.health -= self.damage
        self.cooldown = round(60 / self.attackspeed)
        return target.health