import pygame
import os
from tests import map as map_
from tests import player as player_

pygame.init()
map = map_.Map('map3.png')
done = False
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
player = player_.Player('soldier.png', 16, 16, 4)
clock = pygame.time.Clock()
while not done:
    events = pygame.event.get()
    player.tick(events, map)
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE
            )
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    screen.fill((0, 0, 0))
    surface = pygame.Surface((800, 600))
    map.draw(surface)
    player.draw(surface)
    screen.blit(pygame.transform.scale(surface, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick(60)
