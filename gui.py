import pygame as pg
from resources import gui as img
from resources import font16, hero_data, play
from tooltip import ToolTip

class GUI:
    def __init__(self, player, window_size):
        self.w, self.h = window_size[0] / 800 , window_size[1] / 800
        self.bottom_offset = 60 * self.w
        self.player = player

        self.draw_inventory = True
        self.draw_battlefield = True

        self.inventory_rects = [pg.Rect( ((370 * self.w) + (i // 2) * (68 * self.w), (650*self.h) + (i % 2) * (68*self.h)), (66 * self.w, 66 * self.h) ) for i in range(len(self.player.inventory))]
        self.battlefield_rects = [pg.Rect( ((60 * self.w) + (i // 4) * (68 * self.w), (360*self.h) + (i % 4) * (68*self.h)), (66 * self.w, 66 * self.h) ) for i in range(len(self.player.battlefield))]
        self.buttons = {
            "level_up": [pg.Rect((self.bottom_offset +( 10 * self.w), (682 * self.h)), (54*self.w,46*self.h)), self.player.level_up, ToolTip('Level Up', 'Increase your total population by 1.', self.player.level_up_cost)],
            "reroll":   [pg.Rect((self.bottom_offset +( 10 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.reroll,   ToolTip('Reroll', 'Roll 3 new units. Good Luck!', self.player.roll_cost)],
            "buy_0":    [pg.Rect((self.bottom_offset +( 95 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.buy,      ToolTip((hero_data[self.player.roll[0]]['name']), 'Unit', 1) if self.player.roll[0] else ToolTip('Empty')],
            "buy_1":    [pg.Rect((self.bottom_offset +(155 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.buy,      ToolTip((hero_data[self.player.roll[1]]['name']), 'Unit', 1) if self.player.roll[1] else ToolTip('Empty')],
            "buy_2":    [pg.Rect((self.bottom_offset +(215 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.buy,      ToolTip((hero_data[self.player.roll[2]]['name']), 'Unit', 1) if self.player.roll[2] else ToolTip('Empty')],
        }
        self.selected_surf = pg.Surface((54*self.w,46*self.h))
        self.selected_surf.fill((255,255,255))
        self.selected_surf.set_alpha(64)

        self.clicked_surf = pg.Surface((54*self.w,46*self.h))
        self.clicked_surf.fill((0,0,255))
        self.clicked_surf.set_alpha(128)

        self.hover_surf = pg.Surface((66 * self.w, 36 * self.h)).convert_alpha()
        self.hover_surf.fill((255, 255, 255, 64))
        # self.hover_surf.set_alpha(196)

        self.mouse_holding = None

        for val in img.values():
            val.set_colorkey((255,0,255))

    def update(self, screen):
        mpos = pg.mouse.get_pos()
        screen.blit(img["panel_4"],    (self.bottom_offset, 672 * self.h))
        screen.blit(img["icon_frame"], (self.bottom_offset + (10 * self.w), (682 * self.h)))
        screen.blit(img["level_up"],   (self.bottom_offset + (14 * self.w), (686 * self.h)))

        screen.blit(img["icon_frame"], (self.bottom_offset + 10*self.w, 740*self.h))
        screen.blit(img["reroll"], (self.bottom_offset + 14*self.w, 744*self.h))

        screen.blit(img["gold"], (self.bottom_offset + 75*self.w, 685*self.h))
        screen.blit(font16.render( str(self.player.gold), False, (255,255,255) ), (self.bottom_offset + 105*self.w, 690*self.h))

        screen.blit(img["population"], (self.bottom_offset + 185*self.w, 685*self.h))
        screen.blit(font16.render( f'{len(self.player.battlefield) - self.player.battlefield.count(None)}/{self.player.population}', False, (255,255,255) ), (self.bottom_offset + 215*self.w, 690*self.h))

        for i, card in enumerate(self.player.roll):
            screen.blit(img["icon_frame"], (self.bottom_offset + 95*self.w + (60*self.w)*i, 740*self.h))
            if card:
                screen.blit(img[f"icon_{card}"], (self.bottom_offset + 99*self.w + (60*self.w)*i, 744*self.h))
            else:
                pg.draw.rect(screen, (0,0,0), ( (self.bottom_offset + 99*self.w + (60*self.w)*i, 744*self.h),(46*self.w,38*self.h) ))


        if self.draw_inventory:
            for slot in range(len(self.inventory_rects)):
                if self.inventory_rects[slot].collidepoint(mpos):
                        screen.blit(self.hover_surf, (self.inventory_rects[slot].x, self.inventory_rects[slot].y+30*self.h))
                pg.draw.rect(screen, (255, 255, 255), ((self.inventory_rects[slot].x, self.inventory_rects[slot].y + 30*self.h), (66*self.w,36*self.h)), 2)
                if self.player.inventory[slot]:
                    screen.blit(self.player.inventory[slot].imgs['Standing_S'][0], (self.inventory_rects[slot].x - 40*self.w, self.inventory_rects[slot].y - 40*self.h))
                    screen.blit(img[f'level_{self.player.inventory[slot].level}'], (self.inventory_rects[slot].x, self.inventory_rects[slot].y))
                    if self.player.inventory[slot].health/self.player.inventory[slot].max_health > 0.5:
                        r = int(255 * (1-2*(self.player.inventory[slot].health/self.player.inventory[slot].max_health-0.5)))
                        g = 255
                    else:
                        r = 255
                        g = int(255 * (2*self.player.inventory[slot].health/self.player.inventory[slot].max_health))
                    pg.draw.rect(screen, (10, 10, 10),  ((self.inventory_rects[slot].x + 14*self.w-1, self.inventory_rects[slot].y + 58*self.h-1), (40*self.w+2, 8)))
                    pg.draw.rect(screen, (r, g, 0),     ((self.inventory_rects[slot].x + 14*self.w,   self.inventory_rects[slot].y + 58*self.h), (self.player.inventory[slot].health/self.player.inventory[slot].max_health * 40*self.w, 3)))
                    pg.draw.rect(screen, (30, 60, 200), ((self.inventory_rects[slot].x + 14*self.w,   self.inventory_rects[slot].y + 58*self.h+3), (self.player.inventory[slot].mana/self.player.inventory[slot].max_mana * 40*self.w, 3)))

        if not self.player.in_combat:
            if self.draw_battlefield:
                for slot in range(len(self.battlefield_rects)):
                    if self.battlefield_rects[slot].collidepoint(mpos):
                        screen.blit(self.hover_surf, (self.battlefield_rects[slot].x, self.battlefield_rects[slot].y+30*self.h))
                    pg.draw.rect(screen, (255,60,0), ((self.battlefield_rects[slot].x, self.battlefield_rects[slot].y+30*self.h), (66*self.w,36*self.h)), 2)
                    if self.player.battlefield[slot]:
                        screen.blit(self.player.battlefield[slot].imgs['Standing_S'][0], (self.battlefield_rects[slot].x - 40*self.w, self.battlefield_rects[slot].y - 40*self.h))
                        screen.blit(img[f'level_{self.player.battlefield[slot].level}'], (self.battlefield_rects[slot].x, self.battlefield_rects[slot].y))
                        if self.player.battlefield[slot].health/self.player.battlefield[slot].max_health > 0.5:
                            r = int(255 * (1-2*(self.player.battlefield[slot].health/self.player.battlefield[slot].max_health-0.5)))
                            g = 255
                        else:
                            r = 255
                            g = int(255 * (2*self.player.battlefield[slot].health/self.player.battlefield[slot].max_health))
                        pg.draw.rect(screen, (10, 10, 10),  ((self.battlefield_rects[slot].x + 14*self.w-1,self.battlefield_rects[slot].y + 58*self.h-1), (40*self.w+2, 8)))
                        pg.draw.rect(screen, (r, g, 0),     ((self.battlefield_rects[slot].x + 14*self.w,  self.battlefield_rects[slot].y + 58*self.h), (self.player.battlefield[slot].health/self.player.battlefield[slot].max_health * 40*self.w, 3)))
                        pg.draw.rect(screen, (30, 60, 200), ((self.battlefield_rects[slot].x + 14*self.w,  self.battlefield_rects[slot].y + 58*self.h+3), (self.player.battlefield[slot].mana/self.player.battlefield[slot].max_mana * 40*self.w, 3)))


        if self.mouse_holding:
            x, y = mpos
            screen.blit(self.mouse_holding.imgs['Standing_S'][0], (x-62,y-70) )
            screen.blit(img[f'level_{self.mouse_holding.level}'], (x-30, y-39))

        if mpos[1] > (672*self.h):
            self.check_tooltip(screen, mpos)

    def check_tooltip(self, screen, mpos):
        for val in self.buttons.values():
            if val[0].collidepoint(mpos):
                screen.blit(self.selected_surf, (val[0].topleft))
                val[2].update(screen, mpos)

    def update_buttons(self):
        self.buttons = {
            "level_up": [pg.Rect((self.bottom_offset +( 10 * self.w), (682 * self.h)), (54*self.w,46*self.h)), self.player.level_up, ToolTip('Level Up', 'Increase your total population by 1.', self.player.level_up_cost)],
            "reroll":   [pg.Rect((self.bottom_offset +( 10 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.reroll,   ToolTip('Reroll', 'Roll 3 new units. Good Luck!', self.player.roll_cost)],
            "buy_0":    [pg.Rect((self.bottom_offset +( 95 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.buy,      ToolTip((hero_data[self.player.roll[0]]['name']), 'Unit', 1) if self.player.roll[0] else ToolTip('Empty')],
            "buy_1":    [pg.Rect((self.bottom_offset +(155 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.buy,      ToolTip((hero_data[self.player.roll[1]]['name']), 'Unit', 1) if self.player.roll[1] else ToolTip('Empty')],
            "buy_2":    [pg.Rect((self.bottom_offset +(215 * self.w), (740 * self.h)), (54*self.w,46*self.h)), self.player.buy,      ToolTip((hero_data[self.player.roll[2]]['name']), 'Unit', 1) if self.player.roll[2] else ToolTip('Empty')],
        }

    def click(self, mpos):
        for slot in range(len(self.inventory_rects)):
            if self.inventory_rects[slot].collidepoint(mpos):

                if self.player.inventory[slot] and self.mouse_holding:
                    if self.player.inventory[slot].name == self.mouse_holding.name and self.player.inventory[slot].level == self.mouse_holding.level and self.mouse_holding.level < 4:
                        self.mouse_holding = None
                        self.player.inventory[slot].level_up()
                        self.player.inventory[slot].in_battlefield = False
                    else:
                        self.mouse_holding, self.player.inventory[slot] = self.player.inventory[slot], self.mouse_holding
                        self.mouse_holding.in_battlefield = False
                        self.player.inventory[slot].in_battlefield = False
                
                elif self.player.inventory[slot]:
                    self.mouse_holding = self.player.inventory[slot]
                    self.player.inventory[slot] = None
                    self.mouse_holding.in_battlefield = False

                elif self.mouse_holding:
                    self.player.inventory[slot] = self.mouse_holding
                    self.mouse_holding = None
                    self.player.inventory[slot].in_battlefield = False

        if not self.player.in_combat:
            for slot in range(len(self.battlefield_rects)):
                if self.battlefield_rects[slot].collidepoint(mpos):

                    if self.player.battlefield[slot] and self.mouse_holding:
                        if self.player.battlefield[slot].name == self.mouse_holding.name and self.player.battlefield[slot].level == self.mouse_holding.level and self.mouse_holding.level < 4:
                            self.mouse_holding = None
                            self.player.battlefield[slot].level_up()
                            self.player.battlefield[slot].in_battlefield = True
                        else:
                            self.mouse_holding, self.player.battlefield[slot] = self.player.battlefield[slot], self.mouse_holding
                            self.player.battlefield[slot].in_battlefield = True
                            self.mouse_holding.in_battlefield = False
                    
                    elif self.player.battlefield[slot]:
                        self.mouse_holding = self.player.battlefield[slot]
                        self.player.battlefield[slot] = None
                        self.mouse_holding.in_battlefield = False

                    elif self.mouse_holding:
                        if len(self.player.battlefield) - self.player.battlefield.count(None) < self.player.population:
                            self.player.battlefield[slot] = self.mouse_holding
                            self.mouse_holding = None
                            self.player.battlefield[slot].in_battlefield = True

        flag = False
        for key, val in self.buttons.items():
            if val[0].collidepoint(mpos):
                if key[:3] == 'buy':
                    self.player.buy( int(key[1:].split('_')[1]) )
                else:
                    val[1]()
                flag = True

        if flag:
            self.update_buttons()