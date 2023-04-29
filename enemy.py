import pygame as pg
from hero import Hero
from resources import hero_data
import random

class Enemy:
    def __init__(self, group, scale=1):
        self.group = group
        self.battlefield = [None for i in range(40)]
        self.scale = scale
        
        self.deck = [
                "dwarven_miner",
                "dwarven_rugnur",
                "dwarven_runesmith",
                "dwarven_scout",
                "dwarven_thane",
                "dwarven_thunderer",
                "dwarven_warrior",
            ]

        self.generate(1)

    def generate(self, wave):
        if wave:
            a = random.sample(range(40), k=wave+1)
            for i in a:
                self.battlefield[i] = Hero(self.group, hero_data[random.choice(self.deck)], True, self.scale, int((wave)**(1/2) * random.random()))
                self.battlefield[i].in_battlefield = True


        w, h = self.scale, self.scale
        for i in range(len(self.battlefield)):
            if self.battlefield[i]:
                self.battlefield[i].pos.xy = (60 * w) + (i // 4) * (68 * w)-40, (100*h) + (i % 4) * (68*h)-40

        
        
        
    