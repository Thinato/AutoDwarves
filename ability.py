import pygame as pg
from random import randint

def aoe_heal(origin, target):
    value = randint(int(origin.spell_power * 0.8), int(origin.spell_power * 1.2))    
    


def cast(spell_name:str, origin, target):
    if spell_name and origin.mana >= spells[spell_name][1]:
        origin.mana -= spells[spell_name][1]
        spells[spell_name][0](origin, target)
        return True
    return False
        


spells = {
    'aoe_heal': (aoe_heal, 7000),
}
