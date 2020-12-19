import pygame
from settings import *
from collections import deque
from raycaster import mapping
from numba.core import types
from numba.typed import Dict
from numba import int32
import time


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'sprite_door_v': {
                'sprite': [pygame.image.load(f'sprites/doors/door_v/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_h',
                'obj_action': []
            },
            'sprite_door_h': {
                'sprite': [pygame.image.load(f'sprites/doors/door_h/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_v',
                'obj_action': []
            },
            'sprite_light': {
                'sprite': pygame.image.load('light.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0,
                'scale': (1.3, 1.3),
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': False,
                'is_dead': 'immortal',
                'side': 100,
                'flag': 'light',
                'dead_shift': 0,
                'death_animation': [],
                'obj_action': []

            },
            'sprite_barrel': {
                'sprite': pygame.image.load('barrel.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': (0.4, 0.4),
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 1,
                'blocked': True,
                'is_dead': None,
                'side': 40,
                'flag': 'light',
                'dead_shift': 2,
                'death_animation': deque([pygame.image.load(f'sprites/barrelanim/{i}.png')
                                         .convert_alpha() for i in range(11)]),
                'obj_action': []

            },
            'npc_devil0': {
                'sprite': [pygame.image.load(f'sprites/npc/devil0/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.0,
                'scale': (1.1, 1.1),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/devil0/death/{i}.png')
                                         .convert_alpha() for i in range(6)]),
                'is_dead': 'immortal',
                'dead_shift': 0.6,
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque(
                    [pygame.image.load(f'sprites/npc/devil0/anim/{i}.png').convert_alpha() for i in range(9)]),
            },
            'npc_vampire0': {
                'sprite': pygame.image.load(f'sprites/npc/soldier0/action/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/soldier0/death/{i}.png')
                                         .convert_alpha() for i in range(1)]),
                'is_dead': None,
                'dead_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/npc/soldier0/action/{i}.png')
                                    .convert_alpha() for i in range(3)])
            },


        }
        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['sprite_door_v'], (8.5, 4.5)),
            SpriteObject(self.sprite_parameters['sprite_door_v'], (3.5, 3.5)),
            SpriteObject(self.sprite_parameters['sprite_door_h'], (5.5, 7.5)),
            SpriteObject(self.sprite_parameters['sprite_light'], (5.5, 10)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (6, 10)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (6.3, 10)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (6.3, 10.3)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (6, 10.3)),
            SpriteObject(self.sprite_parameters['sprite_light'], (3, 14)),
            SpriteObject(self.sprite_parameters['sprite_door_v'], (2.5, 9.5)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (3, 9.5)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (3, 9.8)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (3, 9.2)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (10, 3.5)),
            SpriteObject(self.sprite_parameters['npc_vampire0'], (3.5, 13)),
            SpriteObject(self.sprite_parameters['npc_vampire0'], (3.5, 13.3)),
            SpriteObject(self.sprite_parameters['npc_vampire0'], (3.5, 13.6)),
            SpriteObject(self.sprite_parameters['npc_vampire0'], (3.5, 13.9)),



        ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))

    @property
    def blocked_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_objects:
            if obj.flag == 'door_h' or obj.flag == 'door_v':
                if obj.blocked:
                    i, j = mapping(obj.x, obj.y)
                    blocked_doors[(i, j)] = 0
        return blocked_doors


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        # ---------------------
        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # ---------------------
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.side = parameters['side'] # <-------------------------------------------------------
        # self.pos = self.x - self.side // 2, self.y - self.side // 2
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False
        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}


    @property
    def is_on_fire(self):
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return (self.distance_to_sprite, self.proj_height)
        return (float('inf'), None)

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        if self.flag not in {'door_h', 'door_v'}: # <------------------
            self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance_to_sprite),
                                   DOUBLE_HEIGHT if self.flag not in {'door_h', 'door_v'} else HEIGHT) # <--------
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            # logic for doors, npc, decors
            if self.flag == 'door_h' or self.flag == 'door_v':
                if self.door_open_trigger:
                    self.door_open()
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()
            else:
                if self.is_dead and self.is_dead != 'immortal':
                    sprite_object = self.dead_animation()
                    shift = half_sprite_height * self.dead_shift
                    sprite_height = int(sprite_height / 1.3)
                elif self.npc_action_trigger:
                    sprite_object = self.npc_in_action()
                else:
                    # choose sprite for angle
                    self.object = self.visible_sprite()
                    # sprite animation
                    sprite_object = self.sprite_animation()
            # print(sprite_width, sprite_height)
            # if sprite_width > DOUBLE_WIDTH or sprite_height > DOUBLE_HEIGHT:
            #     sprite_rect = sprite_object.get_rect()
            #     kw = sprite_width / WIDTH
            #     kh = sprite_height / HEIGHT
            #     sprite_object = sprite_object.subsurface(sprite_rect.centerx - sprite_rect.w / kw / 2,
            #                                              sprite_rect.centery - sprite_rect.h / kh / 2,
            #                                              sprite_rect.w / kw, sprite_rect.h / kh)
            #     sprite = pygame.transform.scale(sprite_object, (WIDTH, HEIGHT))
            #     sprite_pos = (self.current_ray * SCALE - HALF_WIDTH, HALF_HEIGHT - HALF_HEIGHT + shift)
            # else:
            # sprite scale and pos
            # print(sprite_object if type(sprite_object) == list else 0)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            sprite_pos = (self.current_ray * SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)

            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate(-1)
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object

    def door_open(self):
        if self.flag == 'door_h':
            self.y -= 3
            if abs(self.y - self.door_prev_pos) > TILE:
                self.delete = True

        elif self.flag == 'door_v':
            self.x -= 3
            if abs(self.x - self.door_prev_pos) > TILE:
                self.delete = True







