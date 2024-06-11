"""
Class Cave

Author: Madeleine Neaves
Last modified: 12 May 2024

Represents a cave on the board.
"""

import pygame

from classes.abstract.Position import Position
from classes.enum.Animal import Animal
from classes.enum.Colour import Colour
from classes.utils.image_packager import resource_path


class Cave(Position):
    def __init__(self, coords: tuple[int, int], groups: list[pygame.sprite.Group], animal: Animal, colour: Colour):
        super().__init__(coords, groups, animal)
        self.colour = colour
        self.highlight = False
        self.load_img()

    def load_img(self) -> None:
        """Load the image of the cave
        """
        cave_image = pygame.image.load(self.img_path()).convert_alpha()
        cave_image = pygame.transform.scale(cave_image, (80, 80))

        animal_image = pygame.image.load(self.animal_img_path()).convert_alpha()
        animal_image = pygame.transform.scale(animal_image, (80, 80))

        downward_image = pygame.image.load(self.img_path_arrow()).convert_alpha()
        downward_image = pygame.transform.scale(downward_image, (80, 80))

        if self.highlight == True:
            cave_image.blit(downward_image, (0, 0))
        else:
            cave_image.blit(animal_image, (0, 0))


        self.image = cave_image
        self.rect = cave_image.get_rect(center=self.coords)

    def update(self):
        self.load_img()

    def img_path(self) -> str:
        """gets the path of the image

        Returns:
            str: string of the path
        """
        img_path = f"imgs/caves/{self.colour.name}_CAVE.png"
        return resource_path(img_path)

    def img_path_arrow(self) -> str:
        """gets the path of the corresponding arrow image

        Returns:
            str: string of the path
        """
        img_path = f"imgs/caves/DOWNWARD_CAVE.png"
        return resource_path(img_path)

    def highlight_cave(self) -> None:
        """sets the cave to be highlighted
        """
        self.highlight = True

    def non_highlight_cave(self) -> None:
        """sets the cave to not be highlighted
        """
        self.highlight = False