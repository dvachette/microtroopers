import pygame
import os
from tests import map as map_
from tests import player as player_
from tests import config as config_

pygame.init()
keymap = config_.ConfigKeyMap()
map = map_.Map('map3.png', keymap)
w, h = map.image.get_size()
done = False
screen = pygame.display.set_mode()
player = player_.Player('soldier.png', 16, 16, 4, keymap)
clock = pygame.time.Clock()
zoom = 1
max_zoom = 5
min_zoom = 1
zoom_speed = .1
while not done:
    events = pygame.event.get()
    player.tick(events, map)
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == keymap.key_stop:
                done = True
            if event.key == keymap.key_zoom_in:
                zoom = min(zoom + zoom_speed, max_zoom)
            if event.key == keymap.key_zoom_out:
                zoom = max(zoom - zoom_speed, min_zoom)
    screen.fill((0, 0, 0))
    surface = pygame.Surface(screen.get_size())
    map.draw(surface)
    player.draw(surface)
    surface_zoom = pygame.transform.scale(surface, (int(w * zoom), int(h* zoom)))
    screen.blit(surface_zoom, (0, 0))
    pygame.display.flip()
    clock.tick(60)
