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
            row = ''
            for x in range(10):
                row += str(self.mask.get_at((x, y)))
            print(row)
    def copy(self):
        return self.image.copy()

    def explode(self, center, radius):
        # Créer une surface avec un canal alpha (transparence)
        mask_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)

        # Dessiner un cercle transparent sur la surface
        pygame.draw.circle(mask_surface, (0, 0, 0, 0), center, radius)

        # Dessiner un cercle noir sur la surface pour le masque
        pygame.draw.circle(mask_surface, (0, 0, 0, 255), center, radius)

        # Appliquer la surface du masque à l'image originale
        self.image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.mask = pygame.mask.from_surface(self.image)
