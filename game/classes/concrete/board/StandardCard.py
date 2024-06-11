# Imports
import pygame
from classes.abstract.ChitCard import ChitCard
from classes.enum.Animal import Animal
from classes.utils.file_io import write


class StandardCard(ChitCard):
    def __init__(self, size: int, coordinates: tuple[int, int], groups: list[pygame.sprite.Group], animal: Animal, distance):
        # Pass values to abstract class
        super().__init__(size, coordinates, groups, animal, f'imgs/chits/{animal.name}_{abs(distance)}.png')
        # Concrete attributes
        self.distance = distance

    # Abstract methods
    def save(self) -> None:
        """
        saves the current state of the chit card to a save file
        """
        chit_card = {
            "animal": self.animal.value,
            "type": "standard",
            "distance": self.distance
        }

        write("ChitCards", chit_card)

    # Concrete methods
    def get_destination(self, position=None) -> int:
        return self.distance
