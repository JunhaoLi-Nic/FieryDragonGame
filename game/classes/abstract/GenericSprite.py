"""
Class GenericSprite

GenericSprite is an abstract class that represents a sprite on the board. It is a subclass of pygame.sprite.Sprite.
"""

from abc import ABC, abstractmethod

import pygame


class GenericSprite(pygame.sprite.Sprite):

    def __init__(self, coords: tuple[int, int], groups: list[pygame.sprite.Group]):
        super().__init__(groups)
        self.coords = coords
