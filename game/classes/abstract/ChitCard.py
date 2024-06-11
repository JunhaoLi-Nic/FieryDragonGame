"""
Class ChitCard

Author/s: Madeleine Neaves, Liam Nixon
Last modified: 12 May 2024

Represents a chit card on the board. Can be flipped by clicking.
"""

# Imports
import pygame
from abc import ABC, abstractmethod
from classes.utils.rendering import render_square_image
from classes.abstract.GenericSprite import GenericSprite

# TODO Refactor card rendering
# TODO Refactor card actions


class ChitCard(GenericSprite, ABC):
    def __init__(self, size: int, coordinates: tuple[int, int], groups: list[pygame.sprite.Group], animal, front_image: str) -> None:
        # Configure the GenericSprite abstract class init values
        super().__init__(coordinates, groups)
        # Common attributes
        # Positioning values
        self.abs_x = coordinates[0] * size
        self.abs_y = coordinates[1] * size
        self.abs_pos = (self.abs_x, self.abs_y)
        # Assigned Animal class - using dependency injection
        self.animal = animal
        # Image for the front-side of the card - set by concrete classes
        self.cardFront = render_square_image(front_image, size)
        # Image for the back-side of the card
        self.cardBack = render_square_image('imgs/chits/facedown.png', size)
        # Initially set to face down
        self.image = self.cardBack
        # Get bounds of the ChitCard instance for detecting mouse click events
        self.rect = self.image.get_rect(center=self.abs_pos)
        # Tracks the flipped status of the card
        self.flipped = False

    def get_flipped(self) -> bool:
        return self.flipped

    def update_card(self) -> None:
        """Updates the card image to match the current flipped state
        """
        if self.flipped:
            self.image = self.cardFront
        else:
            self.image = self.cardBack

    def flip_card(self) -> None:
        """
        Inverts the current flipped state of the card
        """
        self.flipped = not self.flipped
        self.update_card()

    def reset_card(self) -> None:
        """
        Ensures that the card is face down when finished with interactions
        """
        self.flipped = False
        self.update_card()

    def card_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Checks if the card was clicked by comparing mouse_pos to the card's position,
            considering the width and height of the card.

        Args:
            mouse_pos (tuple[int, int]): the position of the mouse click

        Returns:
            bool: whether the card was clicked
        """
        if self.rect.collidepoint(mouse_pos):
            return True

    @abstractmethod
    def get_destination(self, position=None) -> int:
        pass

    @abstractmethod
    def save(self) -> None:
        pass
