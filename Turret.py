import pygame as pg

class Turret():
    def __init__(self, pos, damage=20, range=200, attackspeed=2.0, cost=100, cooldown=0):
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos * 40
        pg.draw.circle(self.image, (200,200,0), [20, 20], 15)
        self.pos = pos
        self.damage = damage
        self.range = range
        self.attackspeed = attackspeed
        self.cost = cost
        self.cooldown = cooldown
        self.selected = False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.selected:
            pg.draw.circle(screen, (255,255,255), self.rect.center, self.range, 1)
    
    def save(self):
        return {"position": self.pos.serialize(), "damage": self.damage, "range": self.range, "attackspeed": self.attackspeed, "cost": self.cost, "cooldown": self.cooldown}
    
    def attack(self, target):
        target.health -= self.damage
        self.cooldown = round(60 / self.attackspeed)
        return target.health