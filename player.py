import pygame as pg
from hero import Hero
from random import choices, random
from resources import hero_data, play


class Player:
    def __init__(self, group, deck_type="dwarf", scale=1):
        self.group = group
        self.gold = 3
        self.population = 3
        self.inventory = [None for i in range(12)]
        self.battlefield = [None for i in range(40)]
        self.scale = scale
        self.deck = []
        if deck_type == "dwarf":
            self.deck = [
                "dwarven_miner",
                "dwarven_rugnur",
                "dwarven_runesmith",
                "dwarven_scout",
                "dwarven_thane",
                "dwarven_thunderer",
                "dwarven_warrior",
            ]

        self.modifiers = {
            "crit_rate": 0.1,
            "damage": 0.1,
            "speed": 0.1,
        }

        self.roll_cost = 3
        self.level_up_cost = int(3 + self.population * (self.population / 5))
        self.roll = choices(self.deck, k=3)

        self.mod_roll = choices(list(self.modifiers.keys()), k=3, weights=list(self.modifiers.values()))

        self.in_combat = False

        self.after_combat_delay = 500
        self.after_combat_tick = 0
        self.after_combat = False

        
        


    def level_up(self):
        if self.gold < self.level_up_cost:
            play("error")
            return
        if self.population < len(self.battlefield):
            self.population += 1
            self.gold -= self.level_up_cost
            self.level_up_cost = int(3 + self.population * (self.population / 5))

    def reroll(self):
        if self.gold >= self.roll_cost:
            play("roll")
            self.roll = choices(self.deck, k=3)
            self.gold -= self.roll_cost
        else:
            play("error")

    def reroll_mod(self):
        self.mod_roll = choices(list(self.modifiers.keys()), k=3, weights=list(self.modifiers.values()))
    
    def refresh_buy(self):
        self.roll = choices(self.deck, k=3)


    def buy(self, index):
        if self.roll[index]:
            if self.gold < 1:
                play("error")
                return
            flag = False
            for i in range(len(self.inventory)):
                if not self.inventory[i]:
                    self.inventory[i] = Hero(self.group, hero_data[self.roll[index]], scale=self.scale)
                    flag = True
                    break
            if flag:
                play("buy_unit")
                self.gold -= 1
                self.roll[index] = None
    
    def buy_mod(self, index):
        if self.mod_roll[index]:
            pass

    def apply_mod(self):
        pass

    def start_combat(self, window_scale):
        w, h = window_scale
        for i in range(len(self.battlefield)):
            if self.battlefield[i]:
                self.battlefield[i].pos.xy = (60 * w) + (i // 4) * (68 * w)-40, (360*h) + (i % 4) * (68*h)-40 + (480)*h
                if random() > 0.5:
                    play(self.battlefield[i].sounds['start'])
        self.in_combat = True
    

    def add_gold(self, amount):
        play('coin')
        self.gold += amount

    def heal_fighters(self):
        for hero in self.battlefield:
            if hero:
                hero.heal(.3, True)