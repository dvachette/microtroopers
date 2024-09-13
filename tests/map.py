import pygame
import os


class Map:
    def __init__(self, filename, keymap):
        self.image = pygame.image.load(os.path.join('assets', filename))
        self.mask = pygame.mask.from_surface(self.image)
    def draw(self, screen):
        screen.blit(self.image, (0, 0))
    def print_mask_matrix(self):
        """Used for debugging"""
        width, height = self.mask.get_size()
        for y in range(10):
            row = ""
            for x in range(10):
                row += str(self.mask.get_at((x, y)))
            print(row)