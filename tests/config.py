import dataclasses
import pygame
@dataclasses.dataclass
class ConfigKeyMap:
    key_right:int = pygame.K_d
    key_jump:int = pygame.K_SPACE
    key_left:int = pygame.K_q
    key_stop:int = pygame.K_ESCAPE
    key_zoom_in:int = pygame.K_UP
    key_zoom_out:int = pygame.K_DOWN

@dataclasses.dataclass
class PlayerAttributes:
    frame_width:int = 16
    frame_height:int = 16
    num_frames:int = 4
    current_frame:int = 0
    x:int = 100
    y:int = 0
    delay:int = 100  # Temps en millisecondes entre les frames
    left_pressed:bool = False
    right_pressed:bool = False
    up_pressed:bool = False
    down_pressed:bool = False
    speed:int = 1
    max_fall_speed:int = 5
    gravity:int = 1
    fall_speed:int = 0
    is_jumping:bool = False
    jump_speed:int = 5
    max_jump_speed:int = 5
    falling:bool = False
    step_height:int = 3