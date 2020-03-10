import pygame as pg
from Vector import Vector

class Enemy():
    def __init__(self, position, waypoints, next=None, health=100, totalhealth=100, speed=2, value=20):
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.pos = Vector(position)
        self.waypoints = waypoints
        self.health = health
        self.totalhealth = totalhealth
        self.speed = speed
        self.value = value
        self.selected = False
        if next is None:
            self.next = Vector(self.waypoints.pop(0))
        else:
            self.next = next
        self.nextrect = pg.Rect(self.next * 40, (40, 40))
    
    def draw(self, screen):
        pg.draw.rect(self.image, (255,0,0), (5, 5, 30, 5))
        pg.draw.rect(self.image, (0,255,0), (5, 5, int(30 * self.health / self.totalhealth), 5))
        if self.selected:
            pg.draw.circle(self.image, (255,0,0), (20, 20), 10)
        else:
            pg.draw.circle(self.image, (0,0,0), (20, 20), 10)
        screen.blit(self.image, self.rect)
    
    def getStats(self):
        return ["Health: {}".format(self.health), "Totalhealth: {}".format(self.totalhealth), "Speed: {}".format(self.speed), "Value: {}".format(self.value)]
    
    def save(self):
        return {
            "position": self.pos.serialize(),
            "waypoints": self.waypoints,
            "next": self.next.serialize(),
            "health": self.health,
            "totalhealth": self.totalhealth,
            "speed": self.speed,
            "value": self.value
        }
    
    def move(self):
        vel = (self.next*40 - Vector(self.pos)).normalize()
        self.rect.move_ip(vel * self.speed)
        self.pos = Vector(self.rect.topleft)
        if self.rect.contains(self.nextrect):
            if len(self.waypoints) == 0:
                return True
            self.next = Vector(self.waypoints.pop(0))
            self.nextrect = pg.Rect(self.next * 40, (40, 40))
        return False