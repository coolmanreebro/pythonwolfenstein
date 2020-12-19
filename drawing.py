import pygame
from settings import *
from map import mini_map
from collections import deque
from random import randrange
import sys


class Drawing:
    menu_trigger = True

    def __init__(self, sc, sc_map, player, clock):
        self.sc = sc
        self.sc_map = sc_map
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font('font/font.ttf', 144)
        self.font_vers = pygame.font.Font('font/font.ttf', 36)
        self.textures = {1: pygame.image.load('metal.png').convert(),
                         2: pygame.image.load('bricks.png').convert(),
                         3: pygame.image.load('brickwpainting.png').convert(),
                         4: pygame.image.load('cage.png').convert(),
                         5: pygame.image.load('bricksbad.png').convert(),
                         6: pygame.image.load('brickswblood.png').convert(),
                         7: pygame.image.load('brickswscarypainting.png').convert(),
                         8: pygame.image.load('brickswscarypainting2.png').convert(),
                         'S': pygame.image.load('img/sky0.png').convert(),
                         }
        # menu
        self.menu_trigger = True
        self.music = True
        self.startmusic()
        self.setting_trigger = False
        self.menu_picture = pygame.image.load('img/bg.jpg').convert()
        # weapon parameters
        self.weapon_base_sprite = pygame.image.load('sprites/weapons/shotgun/shot/0.png').convert_alpha()
        self.realsprite = pygame.image.load('sprites/weapons/pistol/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/weapons/shotgun/shot/{i}.png')
                                 .convert_alpha() for i in range(1)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (HALF_WIDTH - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)
        self.shot_length_count = 0
        self.realanimation = deque([pygame.image.load(f'sprites/weapons/pistol/shot/{i}.png')
                                 .convert_alpha() for i in range(2)])
        self.shot_length = len(self.realanimation)
        self.shot_animation_trigger = True
        self.shot_animation_speed = 5
        self.shot_animation_count = 0
        self.fakeanimationcount = 0
        self.shot_sound = pygame.mixer.Sound('sound/pistolsfx.mp3')
        # shot SFX
        self.sfx = deque([pygame.image.load(f'sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)


    def background(self):
        pygame.draw.rect(self.sc, SANDY, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.sc, SCARLETT, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font_vers.render(display_fps, 0, DARKORANGE)
        self.sc.blit(render, FPS_POS)



    def mini_map(self):
        self.sc_map.fill(BLACK)
        map_x, map_y = self.player.x // MAP_SCALE, self.player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), (map_x + 8 * math.cos(self.player.angle),
                                                               map_y + 8 * math.sin(self.player.angle)), 2)
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 4)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, DARKBROWN, (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)

    def player_weapon(self, shot_projections):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shot_projections)[1] // 2
            shot_sprite = self.realanimation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.realanimation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                # self.shot_animation_count = 0
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.realsprite, self.weapon_pos)
        if self.player.opened:
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
                self.player.opened = False
                # self.shot_animation_count = 0
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (HALF_WIDTH - sfx_rect.width // 2, HALF_HEIGHT - sfx_rect.height // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def version(self):
        display_version = "Alpha 1.2.2"
        rplace = self.font_vers.render(display_version, 0, BLACK)
        self.sc.blit(rplace, VERS_POS)

    def startmusic(self):
        pygame.mixer.music.load('sound/newtheme.mp3')
        if self.music == True:
            pygame.mixer.music.play(0)
        elif self.music == False:
            pygame.mixer.music.stop()



    def menu(self):
        x = 0
        y = 0
        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font1.otf', 120)
        settings_font = pygame.font.Font('font/font1.otf', 20)
        start = button_font.render('START', 1, pygame.Color('lightgray'))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.sc.blit(self.menu_picture, (0, 0), (x % WIDTH, y, WIDTH, HEIGHT))
            x += 1
            y += 1

            pygame.draw.rect(self.sc, BLACK, button_start, border_radius=25, width=10)
            self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=25, width=10)
            self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))


            color = randrange(40)
            label = label_font.render('Haunted House', 1, (color, color, color))
            self.sc.blit(label, (220, 100))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, BLACK, button_start, border_radius=25)
                self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    menu_trigger = False
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=25)
                self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()



            pygame.display.flip()
            self.clock.tick(20)









