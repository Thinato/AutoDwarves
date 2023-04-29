import pygame as pg
from resources import font16, font12, gui

class ToolTip:
    def __init__(self, title: str, text: str = '', cost=0):
        self.break_line = 20
        self.title = font16.render(title, False, (255,255,255))
        self.texts = []
        self.size = [self.title.get_width() + 10,28]
        if text:
            self.texts = self.split_text(text)

        self.size[1] += 16 * len(self.texts)

        self.cost = cost
        self.text_cost = font16.render(str(cost), False, (255,255,255))
        if self.cost:
            self.size[1] += 30

    def update(self, screen, mpos):
        pg.draw.rect(screen, (0,0,0), ( (mpos[0], mpos[1] - self.size[1]), self.size ), border_radius=5)
        screen.blit(self.title, (mpos[0] + 5, mpos[1] - self.size[1] + 5))
        for i, text in enumerate(self.texts):
            screen.blit(text, (mpos[0]+ 5, mpos[1] - self.size[1]+28 + (i*14)))
        if self.cost:
            screen.blit(gui['gold_extra'], (mpos[0] + 5, mpos[1] - 30))
            screen.blit(self.text_cost, (mpos[0] + 35, mpos[1] - 26))
        
    def split_text(self, text):
        splitted = text.split()
        res = []
        p = ''
        w = 0
        for word in splitted:
            p += word + ' '
            if len(p) * 14 > w:
                w = len(p) * 14
            if len(p) >= self.break_line:
                res.append(p)
                p = ''
                w = 280
        
        res.append(p)
        if w > self.size[0]:
            self.size[0] = w
        return [font12.render(i, False, (255,255,255)) for i in res ]
