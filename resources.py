import pygame as pg
import json
from random import choice
# don't format this document

def outline(image, color):
    surf = pg.Surface((image.get_width()+2, image.get_height()+2))
    surf.set_colorkey((0,0,0))
    mask = pg.mask.from_surface(image)
    mask = mask.to_surface()
    mask.set_colorkey((0,0,0))
          
    mask_w, mask_h = mask.get_size()
    for x in range(mask_w):
        for y in range(mask_h):
            if mask.get_at((x,y))[0] != 0:
                mask.set_at((x,y), color)

    surf.blit(mask, ( 1, 2))
    surf.blit(mask, ( 2, 1))
    surf.blit(mask, ( 1, 0))
    surf.blit(mask, ( 0, 1))
    return surf

def play(sound):
    choice(sfx[sound]).play()

def scale_imgs(value):
    global gui
    global heroes
    global heroes_outline
    for key, val in gui.items():
        gui[key] = pg.transform.scale_by(val, value)
        
    # for key, val in heroes.items():
    #     heroes[key] = pg.transform.scale_by(val, value)

def get_sounds(hero_name):
    sounds = dict()
    if hero_name in ['Miner', 'Rugnur', 'Runesmith', 'Scout', 'Thane', 'Thunderer', 'Warrior']:
        sounds['death'] = 'dwarf_death'
        sounds['start'] = 'dwarf_start'
    if hero_name in ['Thunderer']:
        sounds['attack'] = 'gun_shot'
    elif hero_name in ['Miner', 'Rugnur', 'Runesmith', 'Thane', 'Warrior', 'Scout']:
        sounds['attack'] = 'sword_hit'
    return sounds

print('loading heroes.json...')
hero_data = json.load( open('heroes.json') )

print('loading GUI...')
gui  = {
    'panel_3':  pg.image.load('assets/img/gui/panel_3.png').convert(),
    'panel_4':  pg.image.load('assets/img/gui/panel_4.png').convert(),
    'icon_frame':  pg.image.load('assets/img/gui/icon_frame.png').convert(),
    'level_up': pg.image.load('assets/img/gui/level_up.png').convert(),
    'reroll':   pg.image.load('assets/img/gui/reroll.png').convert(),
    'icon_dwarven_scout':     pg.image.load('assets/img/gui/heroes/dwarven_scout.png').convert(),
    'icon_dwarven_warrior':   pg.image.load('assets/img/gui/heroes/dwarven_warrior.png').convert(),
    'icon_dwarven_miner':     pg.image.load('assets/img/gui/heroes/dwarven_miner.png').convert(),
    'icon_dwarven_rugnur':    pg.image.load('assets/img/gui/heroes/dwarven_rugnur.png').convert(),
    'icon_dwarven_runesmith': pg.image.load('assets/img/gui/heroes/dwarven_runesmith.png').convert(),
    'icon_dwarven_thane':     pg.image.load('assets/img/gui/heroes/dwarven_thane.png').convert(),
    'icon_dwarven_thunderer': pg.image.load('assets/img/gui/heroes/dwarven_thunderer.png').convert(),
    'gold':   pg.image.load('assets/img/gui/gold.png').convert(),
    'gold_extra':   pg.image.load('assets/img/gui/gold_extra.png').convert(),
    'population':   pg.image.load('assets/img/gui/population.png').convert(),
    'level_1':  pg.image.load('assets/img/gui/level_1.png').convert(),
    'level_2':  pg.image.load('assets/img/gui/level_2.png').convert(),
    'level_3':  pg.image.load('assets/img/gui/level_3.png').convert(),
    'level_4':  pg.image.load('assets/img/gui/level_4.png').convert(),
    'status_bleeding': pg.image.load('assets/img/status_effects/bleeding.png').convert(),
    'status_blessing': pg.image.load('assets/img/status_effects/blessing.png').convert(),
    'status_infusion': pg.image.load('assets/img/status_effects/infusion.png').convert(),
    'status_inspire': pg.image.load('assets/img/status_effects/inspire.png').convert(),
    'status_inspire_extra_1': pg.image.load('assets/img/status_effects/inspire_extra_1.png').convert(),
    'status_precise_shot': pg.image.load('assets/img/status_effects/precise_shot.png').convert(),
    'status_precision': pg.image.load('assets/img/status_effects/precision.png').convert(),
    'status_regeneration': pg.image.load('assets/img/status_effects/regeneration.png').convert(),
    'status_slow': pg.image.load('assets/img/status_effects/slow.png').convert(),
    'status_strength': pg.image.load('assets/img/status_effects/strength.png').convert(),
    'status_stun': pg.image.load('assets/img/status_effects/stun.png').convert(),
    'status_terror': pg.image.load('assets/img/status_effects/terror.png').convert(),
    'status_wither': pg.image.load('assets/img/status_effects/wither.png').convert(),
}

print('loading heroes sprite sheets...')
heroes = {
    'dwarven_scout':     pg.image.load('assets/img/heroes/dwarf/scout.png').convert(),
    'dwarven_warrior':   pg.image.load('assets/img/heroes/dwarf/warrior.png').convert(),
    'dwarven_miner':     pg.image.load('assets/img/heroes/dwarf/miner.png').convert(),
    'dwarven_rugnur':    pg.image.load('assets/img/heroes/dwarf/rugnur.png').convert(),
    'dwarven_runesmith': pg.image.load('assets/img/heroes/dwarf/runesmith.png').convert(),
    'dwarven_thane':     pg.image.load('assets/img/heroes/dwarf/thane.png').convert(),
    'dwarven_thunderer': pg.image.load('assets/img/heroes/dwarf/thunderer.png').convert(),
}

print('loading heroes outlines...')
heroes_outline_enemy = {
    'dwarven_scout':     outline(heroes['dwarven_scout'],     (200,30,30)),
    'dwarven_warrior':   outline(heroes['dwarven_warrior'],   (200,30,30)),
    'dwarven_miner':     outline(heroes['dwarven_miner'],     (200,30,30)),
    'dwarven_rugnur':    outline(heroes['dwarven_rugnur'],    (200,30,30)),
    'dwarven_runesmith': outline(heroes['dwarven_runesmith'], (200,30,30)),
    'dwarven_thane':     outline(heroes['dwarven_thane'],     (200,30,30)),
    'dwarven_thunderer': outline(heroes['dwarven_thunderer'], (200,30,30)),
}
heroes_outline = {
    'dwarven_scout':     outline(heroes['dwarven_scout'],     (30,160,200)),
    'dwarven_warrior':   outline(heroes['dwarven_warrior'],   (30,160,200)),
    'dwarven_miner':     outline(heroes['dwarven_miner'],     (30,160,200)),
    'dwarven_rugnur':    outline(heroes['dwarven_rugnur'],    (30,160,200)),
    'dwarven_runesmith': outline(heroes['dwarven_runesmith'], (30,160,200)),
    'dwarven_thane':     outline(heroes['dwarven_thane'],     (30,160,200)),
    'dwarven_thunderer': outline(heroes['dwarven_thunderer'], (30,160,200)),
}


print('loading fonts...')
font16 = pg.font.Font('assets/font/press_start.ttf', 16)
font12 = pg.font.Font('assets/font/press_start.ttf', 12)

print('loading cursors...')
cursors = {
    'dwarven_0' : pg.image.load('assets/img/cursors/dwarven_gauntlet.png').convert(),
    'dwarven_1' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_1.png').convert(),
    'dwarven_2' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_2.png').convert(),
    'dwarven_3' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_3.png').convert(),
    'dwarven_4' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_4.png').convert(),
    'dwarven_5' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_5.png').convert(),
    'dwarven_6' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_6.png').convert(),
    'dwarven_7' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_7.png').convert(),
    'dwarven_8' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_8.png').convert(),
    'dwarven_9' : pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_9.png').convert(),
    'dwarven_10': pg.image.load('assets/img/cursors/dwarven_gauntlet_extra_10.png').convert(),
    'germanic':   pg.image.load('assets/img/cursors/germanic_hand.png').convert(),
    'gnomish':   pg.image.load('assets/img/cursors/gnomish_glove.png').convert(),
    'goblin': pg.image.load('assets/img/cursors/goblin_gauntlet.png').convert(),
    'teuton': pg.image.load('assets/img/cursors/teuton_gauntlet.png').convert(),
}


print('loading audio...')
sfx = {
    'buy_unit': [pg.mixer.Sound(f'assets/aud/gui/buy_unit-{i}.wav') for i in range(3)],
    'need_gold': [pg.mixer.Sound(f'assets/aud/gui/need_gold.wav')],
    'error': [pg.mixer.Sound(f'assets/aud/gui/error.wav')],
    'roll': [pg.mixer.Sound(f'assets/aud/gui/roll.wav')],
    'gun_shot': [pg.mixer.Sound(f'assets/aud/heroes/attack/gun-{i}.wav') for i in range(3)],
    'sword_hit': [pg.mixer.Sound(f'assets/aud/heroes/attack/sword-{i}.wav') for i in range(6)],
    'dwarf_death': [pg.mixer.Sound(f'assets/aud/heroes/dwarf/death-{i}.wav') for i in range(2)],
    'dwarf_start': [pg.mixer.Sound(f'assets/aud/heroes/dwarf/start-{i}.wav') for i in range(2)],
    'coin': [pg.mixer.Sound(f'assets/aud/gui/coin.wav')],
}

