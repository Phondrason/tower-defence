import pygame as pg

class Button():
    def __init__(self, pos, dimensions, label, centerx=False, centery=False):
        self.width, self.height = dimensions
        self.font = pg.font.SysFont("Calibri", self.height-5)
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((40,40,40))
        pg.draw.rect(self.image, (255,255,255), (0, 0, self.width, self.height), 1)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        if centerx:
            self.rect.centerx = pos[0]
        if centery:
            self.rect.centery = pos[1]
        self.enabled = False
        self.visible = False
        self.label = str(label)
        
    def draw(self, screen):
        if self.visible:
            width, height = self.font.size(self.label)
            if self.enabled:
                rendered = self.font.render(self.label, True, (255,255,255))
            else:
                rendered = self.font.render(self.label, True, (100,100,100))
            self.image.blit(rendered, ((self.width-width)/2, (self.height-height)/2))
            screen.blit(self.image, self.rect)