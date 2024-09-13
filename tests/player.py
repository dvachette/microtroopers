import pygame
import os

if __name__ == '__main__':
    from map import Map
    from config import ConfigKeyMap
else:
    from .map import Map
    from .config import ConfigKeyMap


class Player:
    def __init__(self, filename, frame_width, frame_height, num_frames, keymap):
        self.spritesheet = pygame.image.load(os.path.join('assets', filename))
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.frames = self.load_frames()
        self.frames_right = self.frames
        self.frames_left = [
            pygame.transform.flip(frame, True, False) for frame in self.frames
        ]
        self.current_frame = 0
        self.x = 100
        self.y = 0
        self.mask = pygame.mask.from_surface(self.frames[0])
        self.delay = 100  # Temps en millisecondes entre les frames
        self.last_update = pygame.time.get_ticks()
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 1
        self.max_fall_speed = 5
        self.gravity = 1
        self.fall_speed = 0
        self.is_jumping = False
        self.jump_speed = 5
        self.max_jump_speed = 5
        self.falling = False
        self.step_height = 3
        self.keymap:ConfigKeyMap = keymap
    def load_frames(self):
        frames = []
        for i in range(self.num_frames):
            frame = self.spritesheet.subsurface(
                (0, i * self.frame_height, self.frame_width, self.frame_height)
            )
            frames.append(frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def move(self, x, y):
        self.x += x
        self.y += y

    def left(self, x):
        self.x -= x
        self.frames = self.frames_left

    def right(self, x):
        self.x += x
        self.frames = self.frames_right

    def tick(self, events, map):
        self.update()
        if self.is_jumping:
            self.move(0, -self.jump_speed)
            self.jump_speed -= 1
            if self.jump_speed < 0:
                self.is_jumping = False
                self.jump_speed = self.max_jump_speed

            while self.collides(map):
                self.y += 1
                self.is_jumping = False
        if not (self.on_ground(map) or self.is_jumping):
            self.falling = True
            self.move(0, self.fall_speed)
            self.fall_speed = min(self.fall_speed + self.gravity, self.max_fall_speed)
            while self.collides(map):
                self.y -= 1

        else:
            self.fall_speed = 0
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.keymap.key_left:
                    self.left_pressed = True
                if event.key == self.keymap.key_right:
                    self.right_pressed = True
                if event.key == self.keymap.key_jump:
                    self.up_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == self.keymap.key_left:
                    self.left_pressed = False
                if event.key == self.keymap.key_right:
                    self.right_pressed = False
                if event.key == self.keymap.key_jump:
                    self.up_pressed = False
        if self.left_pressed:
            self.left(self.speed)
            if self.collides(map):
                self.move(0, -self.step_height)
                if self.collides(map):
                    self.move(0, self.step_height)
                    self.move(self.speed, 0)
        if self.right_pressed:
            self.right(self.speed)
            if self.collides(map):
                self.move(0, -self.step_height)
                if self.collides(map):
                    self.move(0, self.step_height)
                    self.move(-self.speed, 0)
        if self.up_pressed:
            if self.on_ground(map):
                self.is_jumping = True

    def collides(self, map):
        if map.mask.overlap(self.mask, (self.x, self.y)):
            return True
        else:
            return False
        
    def on_ground(self, map):
        if map.mask.overlap(self.mask, (self.x, self.y + 1)):
            return True
        else:
            return False