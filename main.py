from player import Player
from sprite_objects import *
from raycaster import ray_casting_walls
from drawing import Drawing
from interaction import Interaction




pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

sc_map = pygame.Surface(MAP_RES)
sprites = Sprites()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock)
interaction = Interaction(player, sprites, drawing)

drawing.menu()



pygame.mouse.set_visible(False)


while True:

    player.movement()
    drawing.background()
    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.version()
    drawing.mini_map()
    drawing.player_weapon([wall_shot, sprites.sprite_shot])

    interaction.interaction_objects()
    interaction.interaction_doors()
    interaction.npc_action()
    interaction.clear_world()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
