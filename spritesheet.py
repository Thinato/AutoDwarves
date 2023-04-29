import pygame as pg
import json
from resources import heroes, heroes_outline, heroes_outline_enemy


class Spritesheet:
    def __init__(self, sheet, json_path, scale: float = 1.0, enemy=False):
        self.sheet = heroes[sheet]
        if enemy:
            self.sheet_outline = heroes_outline_enemy[sheet]
        else:
            self.sheet_outline = heroes_outline[sheet]
        self.scale = scale * 2
        with open("assets/img/sheets/" + json_path) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pg.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sheet, (0, 0), (x, y, w, h))
        return sprite

    def get_sprite_outline(self, x, y, w, h):
        sprite = pg.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sheet_outline, (0, 0), (x, y, w, h))

        return sprite

    def parse_sprite(self, name):
        sprite = self.data["frames"][name]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)

        mask = self.get_sprite_outline(x, y, w, h)
        mask.blit(image, (1, 1))
        return pg.transform.scale(
            mask,
            (
                int(mask.get_width()  * (self.scale)),
                int(mask.get_height() * (self.scale)),
            ),
        )
