import pygame as pg

class Turret():
    def __init__(self, pos, damage=20, range=200, attackspeed=1.0, cost=100):
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = self.pos * 40
        pg.draw.circle(self.image, (200,200,0), [20, 20], 15)
        self.damage = damage
        self.range = range
        self.attackspeed = attackspeed
        self.cost = cost
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pg.draw.circle(screen, (255,255,255), self.rect.center, self.range, 1)
    
    def save(self):
        return {"position": self.pos.serialize(), "damage": self.damage, "range": self.range, "attackspeed": self.attackspeed, "cost": self.cost}