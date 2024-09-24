# Modules
# Low level modules
import os
import time

# Pygame library
import pygame # Used to manage graphics and windows

# High level modules
from tests import map as map_ # Used to manage the map
from tests import player as player_ # Used to manage the player
from tests import config as config_ # Used to manage the configurations


# Initialisation
pygame.init()
# Configurations
keymap = config_.ConfigKeyMap() # Keys configuration
player_attributes = config_.PlayerAttributes() # Players configuration

# Game objects
screen = pygame.display.set_mode()
map = map_.Map('map3.png', keymap)
player = player_.Player('soldier.png', player_attributes, keymap)
clock = pygame.time.Clock()
# TODO Load the background
# background = pygame.image.load(os.path.join('assets', 'OIP.jpeg'))
# background = pygame.transform.scale(background, (screen.get_width()*2, screen.get_height()*2))

# Constants
w, h = map.image.get_size() # Map size
done = False # Game loop
zoom = 1 # Zoom level
max_zoom = 5 # Max zoom level
min_zoom = 1 # Min zoom level
zoom_speed = 0.1 # Zoom speed
ticks = 0 # Ticks counter
now = time.time() # Time counter
center = (0, 0) # Explosion center
radius = 0 # Explosion radius
explode = False # Explosion flag
# Game loop
while not done:
    
    with open('input.txt','r') as f:
        data = f.read()
    with open('input.txt','w') as f:
        f.write('')
    if len(data) > 0:
        data = data.split("\n")
        print(data)
        if data[0] == 'exit':
            done = True
        elif data[0] == "explosion":
            center = (int(data[1]), int(data[2]))
            radius = int(data[3])
            explode = True
    if explode:
        map.explode(center, radius)
        explode = False
    
    events = pygame.event.get() # Events
    player.tick(events, map) # Player tick
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == keymap.key_stop:
                done = True
            # Zoom in and out
            if event.key == keymap.key_zoom_in:
                zoom = min(zoom + zoom_speed, max_zoom)
            if event.key == keymap.key_zoom_out:
                zoom = max(zoom - zoom_speed, min_zoom)
    screen.fill((0, 0, 255)) # Reset screen
    surface = map.image.copy() # Surface where the map will be drawn
    map.draw(surface) # Draw the map
    player.draw(surface) # Draw the player
    surface_zoom = pygame.transform.scale(
        surface, (int(w * zoom), int(h * zoom))
    ) # Zoom the surface
    position_player = ((player.x+8)*zoom, (player.y+8)*zoom) # Player position
    center = (screen.get_width() // 2, screen.get_height() // 2) # Center of the screen
    
    final = (
        center[0] - position_player[0],
        center[1] - position_player[1],
    ) # Final position of the surface

    # For debugging
    if time.time() - now > 1:
        print(f'{center=}, {position_player=}, {final=}')
        now = time.time()
    # TODO Draw the background
    screen.blit(surface_zoom, final) # Draw the zoomed surface
    pygame.display.flip() # Update the screen
    clock.tick(60) # FPS

