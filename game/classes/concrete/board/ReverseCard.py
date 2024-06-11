# Imports
import pygame
from classes.abstract.ChitCard import ChitCard
from classes.enum.Animal import Animal
from classes.utils.file_io import write


class ReverseCard(ChitCard):
    def __init__(self, size: int, coordinates: tuple[int, int], groups: list[pygame.sprite.Group], animal: Animal):
        # Pass values to abstract class
        super().__init__(size, coordinates, groups, animal, f'imgs/chits/{animal.name}.png')

    # Abstract methods
    def save(self) -> None:
        pass

    # Concrete methods
    def find_nearest_cave(self, position) -> int:
        return position.nearest_cave([], [], position)

    # Implement abstract methods
    def get_destination(self, position=None) -> int:
        if position:
            return self.find_nearest_cave(position)
        else:
            return 0

    def save(self) -> None:
        """
        saves the current state of the chit card to a save file
        """
        chit_card = {
            "animal": self.animal.value,
            "type": "reverse"
        }

        write("ChitCards", chit_card)
