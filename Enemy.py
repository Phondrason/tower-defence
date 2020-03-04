import pygame as pg
from Vector import Vector

class Enemy():
    def __init__(self, position, waypoints, next=None, health=100, speed=5):
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        pg.draw.circle(self.image, (0,0,0), [20, 20], 10)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.health = health
        self.speed = speed
        self.waypoints = waypoints
        if next is None:
            self.next = Vector(self.waypoints.pop(0))
        else:
            self.next = next
        self.nextrect = pg.Rect(self.next * 40, (40, 40))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def save(self):
        return {"health": self.health, "speed": self.speed, "waypoints": self.waypoints, "position": Vector(self.rect.topleft).serialize(), "next": self.next.serialize()}
    
    def move(self):
        vel = (self.next*40 - Vector(self.rect.topleft)).normalize()
        self.rect.move_ip(vel * self.speed)
        if self.rect.contains(self.nextrect):
            if len(self.waypoints) == 0:
                return True
            self.next = Vector(self.waypoints.pop(0))
            self.nextrect = pg.Rect(self.next * 40, (40, 40))
        return False