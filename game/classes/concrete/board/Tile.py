"""
Class Tile

Author: Madeleine Neaves
Last modified: 12 May 2024
"""

import pygame

from classes.abstract.Position import Position
from classes.enum.Animal import Animal


class Tile(Position):
    def __init__(self, coords: tuple[int, int], groups: list[pygame.sprite.Group], animal: Animal):
        super().__init__(coords, groups, animal)
        self.load_img()

    def load_img(self) -> None:
        """Load the image of the tile
        
        """
        self.image = pygame.image.load(self.animal_img_path()).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=self.coords)
