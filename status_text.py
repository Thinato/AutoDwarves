import pygame as pg
from resources import font16, font12

class StatusText(pg.sprite.Sprite):
    def __init__(self, group, text:str, pos, color=(255,255,255), duration=600, static=False, battlefield=True):
        super().__init__(group)
        self.static = static
        self._circle_cache = {}
        self.text = self.render(text, font12, color)
        self.speed = 50
        self.pos = pg.math.Vector2(pos) - (self.text.get_width()/2, self.text.get_height()/2)
        self.duration = pg.time.get_ticks() + duration
        self.in_battlefield = battlefield
        


    def update(self, screen, dt, camera):
        if pg.time.get_ticks() > self.duration:
            self.kill()
        self.pos.y -= self.speed * dt
        if self.static:
            screen.blit(self.text, self.pos)
        else:
            screen.blit(self.text, self.pos - camera)

    def _circlepoints(self, r):
        r = int(round(r))
        if r in self._circle_cache:
            return self._circle_cache[r]
        x, y, e = r, 0, 1 - r
        self._circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def render(self, text, font, gfcolor=(255,255,255), ocolor=(0,0,0), opx=1):
        textsurface = font.render(text, True, gfcolor).convert_alpha()
        w = textsurface.get_width() + 2 * opx
        h = font.get_height()

        osurf = pg.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

        for dx, dy in self._circlepoints(opx):
            surf.blit(osurf, (dx + opx, dy + opx))

        surf.blit(textsurface, (opx, opx))
        return surf