import pygame as pg

class MenuManager:
    def __init__(self):
        self.selectedIndex = 0
        self.selColor = (255,255,0)
        self.desColor = (255,255,255)

    def drawMenu(self, screen):
        for i, opt in enumerate(self.rendered["des"]):
            opt[1].center = (self.screenRect.centerx, self.fromBottom + i*self.spacer)
            if i == self.selectedIndex:
                rendImg, rendRect = self.rendered["sel"][i]
                rendRect.center = opt[1].center
                screen.blit(rendImg, rendRect)
            else:
                screen.blit(opt[0], opt[1])

    def updateMenu(self):
        self.changeSelectedOption()

    def getEventMenu(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_w]:
                self.changeSelectedOption(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.changeSelectedOption(1)
            elif event.key == pg.K_RETURN:
                self.selectOption(self.selectedIndex)
        self.mouseMenuClick(event)

    def mouseMenuClick(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i, opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selectedIndex = i
                    self.selectOption(i)
                    break

    def preRenderOptions(self):
        fontDeselect = pg.font.SysFont("arial", 50)
        fontSelect = pg.font.SysFont("arial", 70)

        renderedMsg = {"des": [], "sel": []}
        for option in self.options:
            d_rend = fontDeselect.render(option, 1, self.desColor)
            d_rect = d_rend.get_rect()
            s_rend = fontSelect.render(option, 1, self.selColor)
            s_rect = s_rend.get_rect()
            renderedMsg["des"].append((d_rend, d_rect))
            renderedMsg["sel"].append((s_rend, s_rect))
        self.rendered = renderedMsg

    def selectOption(self, i):
        if i == len(self.nextList):
            self.quit = True
        else:
            self.next = self.nextList[i]
            self.done = True
            self.selectedIndex = 0

    def changeSelectedOption(self, op=0):
        for i, opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                self.selectedIndex = i
        if op:
            self.selectedIndex += op
            maxInd = len(self.rendered["des"])-1
            if self.selectedIndex < 0:
                self.selectedIndex = maxInd
            elif self.selectedIndex > maxInd:
                self.selectedIndex = 0
