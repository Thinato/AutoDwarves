import pygame as pg
from utility import dist

pg.init()
clock = pg.time.Clock()
window = pg.display.set_mode((640,640))
screen = pg.Surface((800,800))

from resources import cursors, font16, scale_imgs

scale_imgs(window.get_size()[0] / 800)

from gui import GUI
from player import Player
from enemy import Enemy
from hero import Hero


cursor = cursors['dwarven_0']
pg.mouse.set_visible(False)

all_sprites = pg.sprite.Group()
gui_group = pg.sprite.Group()
player = Player(all_sprites, scale=window.get_size()[0] / 800)
enemy  = Enemy(all_sprites, scale=window.get_size()[0] / 800)
gui = GUI(player, window.get_size())

back_ph = pg.image.load('assets/img/maps/forest.png').convert()
back_ph = pg.transform.scale(back_ph, (window.get_size()[0],1280 * (window.get_size()[1]/800)))

camera = pg.math.Vector2(0, back_ph.get_size()[1]-window.get_size()[1])
camera_speed = 3800

wave = 1

def finish_combat(player, enemy):
    global wave
    player.in_combat = False
    wave += 1
    enemy.generate(wave)
    player.refresh_buy()
    
    player.after_combat_tick = pg.time.get_ticks()
    player.after_combat = True

    return pg.math.Vector2(0, back_ph.get_size()[1]-window.get_size()[1])





while True:
    dt = clock.tick() / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                gui.click(pg.mouse.get_pos())
            if player.in_combat:
                if event.button == 4:
                    camera.y -= camera_speed * dt
                    if camera.y < 0:
                        camera.y = 0
                if event.button == 5:
                    camera.y += camera_speed * dt
                    if camera.y > back_ph.get_size()[1] - window.get_size()[1]:
                        camera.y = back_ph.get_size()[1] - window.get_size()[1]

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                player.reroll()
                gui.update_buttons()
            elif event.key == pg.K_f:
                player.level_up()
            elif event.key == pg.K_1:
                player.buy(0)
                gui.update_buttons()
            elif event.key == pg.K_2:
                player.buy(1)
                gui.update_buttons()
            elif event.key == pg.K_3:
                player.buy(2)
                gui.update_buttons()
            elif event.key == pg.K_SPACE:
                player.start_combat((window.get_size()[0]/800, window.get_size()[0]/800))
            elif event.key == pg.K_LSHIFT:
                camera_speed = 11400
            elif event.key == pg.K_k:
                for i in range(40):
                    if player.battlefield[i]:
                        player.battlefield[i].modifiers["crit_rate"] += 5
                        print('hero blessed!')
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LSHIFT:
                camera_speed = 3800
        
    screen.fill((255,0,255))


    screen.blit(back_ph, (0,0) - camera)
 
    if player.after_combat and pg.time.get_ticks() > player.after_combat_delay + player.after_combat_tick:
        for i, hero in enumerate(player.battlefield):
            if hero:
                hero.heal(.3, True, index=i, group=gui_group)

        player.add_gold(5)
        player.after_combat = False


    if player.in_combat:
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            camera.y -= camera_speed/10 * dt
            if camera.y < 0:
                camera.y = 0
        elif keys[pg.K_DOWN]:
            camera.y += camera_speed/10 * dt
            if camera.y > back_ph.get_size()[1] - window.get_size()[1]:
                camera.y = back_ph.get_size()[1] - window.get_size()[1]
        for sprite in sorted(all_sprites.sprites(), key = lambda sprite: sprite.pos.y):
            if sprite.in_battlefield:
                if enemy.battlefield.count(None) == len(enemy.battlefield):
                    camera = finish_combat(player, enemy)

                if isinstance(sprite, Hero):
                    for sprite2 in all_sprites.sprites():
                        if sprite != sprite2 and isinstance(sprite2, Hero):
                            if pg.sprite.collide_rect(sprite, sprite2):
                                sprite.pos.x -= (sprite2.rect.centerx - sprite.rect.centerx) * dt * 1.5
                                sprite.pos.y -= (sprite2.rect.centery - sprite.rect.centery) * dt * 1.5


                    if not sprite.target:
                        if sprite.enemy:
                            nearest = None
                            for hero in player.battlefield:
                                if hero and nearest and dist(sprite, hero) < dist(sprite, nearest):
                                    nearest = hero
                                elif hero and not nearest:                         
                                    nearest = hero
                            sprite.target = nearest
                            if nearest:
                                nearest.target_of.append(sprite)
                        else:                                
                            nearest = None
                            for hero in enemy.battlefield:
                                if hero and nearest and dist(sprite, hero) < dist(sprite, nearest):
                                    nearest = hero
                                elif hero and not nearest:                         
                                    nearest = hero
                            sprite.target = nearest
                            if nearest:
                                nearest.target_of.append(sprite)
                            

                    if sprite.enemy and sprite.dead:
                        for hero in sprite.target_of:
                            hero.target = None
                        enemy.battlefield[enemy.battlefield.index(sprite)] = None
                        player.add_gold(1)
                        sprite.kill()

                    elif sprite.dead:
                        for hero in sprite.target_of:
                            hero.target = None
                        player.battlefield[player.battlefield.index(sprite)] = None
                        sprite.kill()
                sprite.update(screen, dt, camera)

    gui.update(screen)
    gui_group.update(screen, dt, camera)

    window.blit(screen, (0,0))
    window.blit(cursor, pg.mouse.get_pos())
    window.blit(font16.render( str(round(clock.get_fps(),2)), True, (255, 255, 255), (0, 0, 0) ), (0,0))
    pg.display.flip()
