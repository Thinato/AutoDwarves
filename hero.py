import pygame as pg
from resources import heroes, gui, get_sounds, play
from spritesheet import Spritesheet
from math import sin, cos, atan2
from random import random, randint
from status_text import StatusText
from ability import cast


class Hero(pg.sprite.Sprite):
    def __init__(self, group, data, enemy = False, scale=1, level=1):
        super().__init__(group)
        if level < 1:
            level = 1
        elif level > 4:
            level = 4
        self.modifiers = {
            "crit_rate":0,
            "health": 0,
            "damage": 0,
            "speed": 0,
        }
        self.group = group
        self.scale = scale
        self.name = data.get("name", "unnamed")
        self.max_health = data.get("health", 100)
        self.health = self.max_health
        self.max_mana = data.get("mana", 100)
        self.mana = data.get("initial_mana", 0)
        self.mana_regen = data.get("mana_regen", 10)
        self.armor = data.get("armor", 10)
        self.speed = data.get("speed", 40)
        self.damage = data.get("damage", 15)
        self.struct_damage = data.get("struct_damage", 10)
        self.crit_rate = data.get("crit_rate", 0.1)
        self.spell_power = data.get("spell_power", 10)
        self.spell = data.get('spell', '')


        self.attack_range = data.get("range", 60)
        self.attack_speed = data.get("atk_speed", 1000)
        self.attack_last = 0

        self.in_battlefield = False

        self.pos = pg.math.Vector2(0, 0)
        self.enemy = enemy

        self.rect = pg.Rect(self.pos + (52*self.scale, 52*self.scale), (40*self.scale, 40*self.scale))

        self.data = data
        self.ss = Spritesheet(
            data.get("img_path", "dwarf/scout.png"), "hero.json", scale, enemy
        )
        self.imgs = {
            "Standing_N":  [self.ss.parse_sprite("Standing_N-0")],
            "Standing_NE": [self.ss.parse_sprite("Standing_NE-0")],
            "Standing_E":  [self.ss.parse_sprite("Standing_E-0")],
            "Standing_SE": [self.ss.parse_sprite("Standing_SE-0")],
            "Standing_S":  [self.ss.parse_sprite("Standing_S-0")],
            
            "Standing_NW": [pg.transform.flip(self.ss.parse_sprite("Standing_NE-0"), True, False)],
            "Standing_W":  [pg.transform.flip(self.ss.parse_sprite("Standing_E-0") , True, False)],
            "Standing_SW": [pg.transform.flip(self.ss.parse_sprite("Standing_SE-0"), True, False)],

            "Running_N":  [self.ss.parse_sprite(f"Running_N-{i}")  for i in range(4)],
            "Running_NE": [self.ss.parse_sprite(f"Running_NE-{i}") for i in range(4)],
            "Running_E":  [self.ss.parse_sprite(f"Running_E-{i}")  for i in range(4)],
            "Running_SE": [self.ss.parse_sprite(f"Running_SE-{i}") for i in range(4)],
            "Running_S":  [self.ss.parse_sprite(f"Running_S-{i}")  for i in range(4)],

            "Running_NW": [pg.transform.flip(self.ss.parse_sprite(f"Running_NE-{i}") , True, False ) for i in range(4)],
            "Running_W":  [pg.transform.flip(self.ss.parse_sprite(f"Running_E-{i}") , True, False ) for i in range(4)],
            "Running_SW": [pg.transform.flip(self.ss.parse_sprite(f"Running_SE-{i}") , True, False ) for i in range(4)],

            "Attacking_N":  [self.ss.parse_sprite(f"Attacking_N-{i}")  for i in range(4)],
            "Attacking_NE": [self.ss.parse_sprite(f"Attacking_NE-{i}") for i in range(4)],
            "Attacking_E":  [self.ss.parse_sprite(f"Attacking_E-{i}")  for i in range(4)],
            "Attacking_SE": [self.ss.parse_sprite(f"Attacking_SE-{i}") for i in range(4)],
            "Attacking_S":  [self.ss.parse_sprite(f"Attacking_S-{i}")  for i in range(4)],

            "Attacking_NW": [pg.transform.flip(self.ss.parse_sprite(f"Attacking_NE-{i}") , True, False ) for i in range(4)],
            "Attacking_W":  [pg.transform.flip(self.ss.parse_sprite(f"Attacking_E-{i}") , True, False ) for i in range(4)],
            "Attacking_SW": [pg.transform.flip(self.ss.parse_sprite(f"Attacking_SE-{i}") , True, False ) for i in range(4)],
            
        }
        self.sounds = get_sounds(self.name)

        self.cur_img = "Standing_S"
        self.target = None
        self.direction = pg.math.Vector2()
        self.dead = False
        self.target_of = []

        self.last_anim = 0
        self.tick_anim = 200
        self.cur_anim  = 0
        self.last_angle = 0
        
        self.level = level
        if self.level > 1:
            for i in range(level-1):
                self.level_up()


    def update(self, screen, dt, camera):
        self.rect.topleft = self.pos.xy + (52*self.scale, 52*self.scale)
        if self.target:
            if (
                (self.pos.x - self.target.pos.x) ** 2
                + (self.pos.y - self.target.pos.y) ** 2
            ) ** (1 / 2) > self.attack_range:
                angle = atan2( (self.target.pos.y - self.pos.y ), (self.target.pos.x - self.pos.x) )
                self.last_angle = angle
                self.direction.xy = cos(angle), sin(angle)
                self.move(angle, dt)
            elif pg.time.get_ticks() > self.attack_last + self.attack_speed:
                angle = atan2( (self.target.pos.y - self.pos.y ), (self.target.pos.x - self.pos.x) )
                self.last_angle = angle
                self.attack_last = pg.time.get_ticks()
                self.attack(angle)
        else:
            self.cur_img = 'Standing_' + self.cur_img.split('_')[1]
            self.cur_anim = 0

        if pg.time.get_ticks() > self.last_anim:
            self.last_anim = pg.time.get_ticks() + self.tick_anim
            self.cur_anim += 1
            if self.cur_anim >= len(self.imgs[self.cur_img]):
                self.cur_anim = 0

        screen.blit(self.imgs[self.cur_img][self.cur_anim], self.pos - camera)
        # health bar #
        if self.health > 0:
            if self.health/self.max_health > 0.5:
                r = int(255 * (1-2*(self.health/self.max_health-0.5)))
                g = 255
            else:
                r = 255
                g = int(255 * (2*self.health/self.max_health))
            pg.draw.rect(screen, (10, 10, 10), (self.pos-camera + (52*self.scale-1, 94*self.scale-1), (40*self.scale+2, 8)))
            pg.draw.rect(screen, (r, g, 0), (self.pos-camera + (52*self.scale, 94*self.scale), (self.health/self.max_health * 40*self.scale, 3)))
            pg.draw.rect(screen, (30, 60, 200), (self.pos-camera + (52*self.scale, 94*self.scale+3), (self.mana/self.max_mana * 40*self.scale, 3)))

        screen.blit(gui[f'level_{self.level}'], (self.pos - camera + (33,32)))
        # pg.draw.rect(screen, (0,255,0), (self.rect.topleft - camera, self.rect.size), 1)

    def move(self, angle, dt):
        if angle < -2.75:
            self.cur_img = 'Running_W'
        elif angle < -1.96:
            self.cur_img = 'Running_NW'
        elif angle < -1.18:
            self.cur_img = 'Running_N'
        elif angle < -0.39:
            self.cur_img = 'Running_NE'
        elif angle < 0.39:
            self.cur_img = 'Running_E'
        elif angle < 1.18:
            self.cur_img = 'Running_SE'
        elif angle < 1.96:
            self.cur_img = 'Running_S'
        elif angle < 2.75:
            self.cur_img = 'Running_SW'
        else:
            self.cur_img = 'Running_W'

        self.tick_anim = self.speed * 5
        

        if self.direction.magnitude() > 0:
            self.pos += self.direction.normalize() * dt * self.speed

    def hit(self, damage):
        dmg = damage - self.armor
        if dmg <= 0:
            dmg = 1
        StatusText(self.group, str(-dmg), (self.pos.x + 144*self.scale/2,self.pos.y + 144*self.scale/2), (255, randint(140,210), 0) )
        self.health -= dmg
        if self.health <= 0:
            self.dead = True
            play(self.sounds['death'])

            

    def attack(self, angle):
        if angle < -2.75:
            self.cur_img = 'Attacking_W'
        elif angle < -1.96:
            self.cur_img = 'Attacking_NW'
        elif angle < -1.18:
            self.cur_img = 'Attacking_N'
        elif angle < -0.39:
            self.cur_img = 'Attacking_NE'
        elif angle < 0.39:
            self.cur_img = 'Attacking_E'
        elif angle < 1.18:
            self.cur_img = 'Attacking_SE'
        elif angle < 1.96:
            self.cur_img = 'Attacking_S'
        elif angle < 2.75:
            self.cur_img = 'Attacking_SW'
        else:
            self.cur_img = 'Attacking_W'
        

        self.tick_anim = self.attack_speed // 4

        play(self.sounds['attack'])

        i, j = int((self.damage + self.modifiers["damage"]) *0.85), int((self.damage + self.modifiers["damage"]) * 1.15)
        if random() < self.crit_rate + (self.modifiers["crit_rate"]*0.01):
            i, j = i*2, j*2
        dmg = randint(i,j)

        if not cast(self.spell, self, self):
            self.target.hit( dmg )
            self.gain_mana(self.mana_regen, False)
        

    def level_up(self):
        if self.level < 4:
            self.max_health *= 1.4
            self.health = self.max_health
            self.damage *= 1.4
            self.spell_power *= 1.4
            self.level += 1
            StatusText(self.group, f'Level Up!', (self.pos.x + 144*self.scale/2, self.pos.y + 144*self.scale/2), (255, 170, 20) )
            
    
    def heal(self, amount, percent=False, index=-1, group=None):
        if index > -1:
            pos = (91 * self.scale) + (index // 4) * (68 * self.scale), (393*self.scale) + (index % 4) * (68*self.scale)
            static = True
        else:
            static = False
            pos = (self.pos.x + 144*self.scale/2,self.pos.y + 144*self.scale/2)
        if percent:
            self.health += int(self.max_health * amount)
            # StatusText(group if group else self.group, f'+{self.max_health * amount}', pos, (30, 180, 20), static=static)
            StatusText(group, f'+{int(self.max_health * amount)}', pos, (30, 180, 20), static=static)
        else:
            self.health += amount
            StatusText(group if group else self.group, f'+{amount}', pos, (30, 180, 20), static=static)
            
        
        if self.health > self.max_health:
            self.health = self.max_health
    
    def gain_mana(self, amount, status=True):
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        elif status:
            StatusText(self.group, f'+{amount}', (self.pos.x + 144*self.scale/2, self.pos.y + 144*self.scale/2), (50, 135, 255) )

    def set_modifiers(self, modifiers):
        self.modifiers = modifiers
        


        
