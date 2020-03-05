import pygame as pg
from Turret import Turret
from Enemy import Enemy
from Vector import Vector

class Board():
    def __init__(self):
        self.font = pg.font.SysFont("Calibri", 50)
        self.image = pg.Surface((800, 600))
        self.image.fill((70,155,30))
        self.rect = self.image.get_rect()
        self.matrix = [["empty" for x in range(20)] for y in range(15)]
        self.waypoints = [[1,0],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[18,2],[18,3],[17,3],[16,3],[15,3],[14,3],[13,3],[12,3],[11,3],[10,3],[9,3],[8,3],[7,3],[6,3],[5,3],[4,3],[3,3],[2,3],[1,3],[1,4],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],[9,5],[10,5],[11,5],[12,5],[13,5],[14,5],[15,5],[16,5],[17,5],[18,5],[18,6],[18,7],[17,7],[16,7],[15,7],[14,7],[13,7],[12,7],[11,7],[10,7],[9,7],[8,7],[7,7],[6,7],[5,7],[4,7],[3,7],[2,7],[1,7],[1,8],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],[10,9],[11,9],[12,9],[13,9],[14,9],[15,9],[16,9],[17,9],[18,9],[18,10],[18,11],[17,11],[16,11],[15,11],[14,11],[13,11],[12,11],[11,11],[10,11],[9,11],[8,11],[7,11],[6,11],[5,11],[4,11],[3,11],[2,11],[1,11],[1,12],[1,13],[2,13],[3,13],[4,13],[5,13],[6,13],[7,13],[8,13],[9,13],[10,13],[11,13],[12,13],[13,13],[14,13],[15,13],[16,13],[17,13],[18,13],[18,14]]
        for x, y in self.waypoints: 
            self.matrix[y][x] = "path"
            pg.draw.rect(self.image, (214,148,27), (x*40, y*40, 40, 40))
        self.enemies = self.spawnWave()
        self.spawnTimer = 1800
        self.turrets = []

    def spawnWave(self):
        return [Enemy(Vector(40, -40*i), self.waypoints[:], health=100, totalhealth=100, speed=2) for i in range(1, 11)]

    def load(self, dict):
        self.matrix = dict["matrix"]
        self.turrets = [Turret(Vector(turret["position"]), turret["damage"], turret["range"], turret["attackspeed"], turret["cost"], turret["cooldown"]) for turret in dict["turrets"]]
        self.enemies = [Enemy(Vector(enemy["position"]), enemy["waypoints"], Vector(enemy["next"]), enemy["health"], enemy["totalhealth"], enemy["speed"]) for enemy in dict["enemies"]]
    
    def save(self):
        return {
            "matrix": self.matrix,
            "turrets": [turret.save() for turret in self.turrets],
            "enemies": [enemy.save() for enemy in self.enemies]
        }

    def click(self, pos):
        x, y = pos // 40
        if self.matrix[y][x] == "empty":
            self.matrix[y][x] = "turret"
            self.turrets.append(Turret(pos // 40))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for enemy in self.enemies:
            enemy.draw(screen)
        for turret in self.turrets:
            turret.draw(screen)
        rendered = self.font.render(str(round(self.spawnTimer / 60, 1)), True, (255,255,255))
        screen.blit(rendered, (20, 20))
    
    def update(self):
        self.spawnTimer -= 1
        for enemy in self.enemies:
            if enemy.move():
                print("rip")
        for turret in self.turrets:
            turret.cooldown -= 1
            if turret.cooldown <= 0:
                eligible = [enemy for enemy in self.enemies if (Vector(enemy.rect.center) - Vector(turret.rect.center)).norm() <= turret.range]
                if len(eligible) > 0:
                    target = min(eligible, key=lambda enemy: len(enemy.waypoints))
                    if turret.attack(target) < 0:
                        self.enemies.remove(target)
        if len(self.enemies) == 0 or self.spawnTimer == 0:
            self.enemies.extend(self.spawnWave())
            self.spawnTimer = 1800