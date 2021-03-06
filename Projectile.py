from Vector import Vector
import pygame as pg

class Projectile():
    def __init__(self, origin, target):
        self.image = pg.Surface((7,7), pg.SRCALPHA)
        pg.draw.circle(self.image, (255,255,255), (3,3), 3)
        self.rect = self.image.get_rect()
        self.pos = Vector(origin.rect.center)
        self.rect.center = self.pos
        self.target = target
        self.speed = 20
    
    def update(self):
        x, y = (self.target.pos - self.pos).normalize() * self.speed
        self.rect.move_ip(x, y)
        self.pos = Vector(self.rect.center)
        return (self.target.pos - self.pos).norm() <= 10
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)