"""
Class Position

Author: Madeleine Neaves
Last modified: 12 May 2024

Represents a position on the board that has an animal.
"""

from abc import ABC, abstractmethod

import pygame.sprite
from classes.enum.Animal import Animal
from classes.abstract.GenericSprite import GenericSprite
from classes.utils.image_packager import resource_path


class Position(GenericSprite, ABC):
    def __init__(self, coords: tuple[int, int], groups: list[pygame.sprite.Group], animal: Animal):
        super().__init__(coords, groups)
        self.animal = animal
        self.occupied = False
        self.previous_position = None
        self.next_position = None
        self.attached_cave = None

    def is_occupied(self) -> bool:
        """
        Returns whether the position is occupied by a token.
        
        Args:
            None
        Returns:
            bool: True if the position is occupied, False otherwise
        """
        return self.occupied

    def animal_img_path(self):
        """gets the path of the image of the animal

        Returns:
            resource_path: resource path of the image
        """
        animal_name = self.animal.value
        img_path = f"imgs/animals/{animal_name}.png"
        return resource_path(img_path)

    def nearest_cave(self, distance_results, position_results, starting_position, current_position = None, distance: int = 0, found: bool = False, direction: bool = False, max_depth: int = 50):
        # If the current position has not been set, default to the starting position
        if not current_position:
            current_position = starting_position
        if found:
            """
            # Record the distance travelled to reach the position
            distance_results.append(distance)
            position_results.append(current_position.attached_cave)
            # Check if a result in both directions has been found
            if len(distance_results) < 2:
                # Start looking again, in the other direction
                return self.nearest_cave(distance_results, position_results, starting_position, starting_position, 0,
                                         False, not direction)
            else:
                # Return the shortest of the two distances, maintaining negative distance for backwards direction
                if abs(distance_results[0]) < abs(distance_results[1]):
                    return distance_results[0], position_results[0]
                else:
                    return distance_results[1], position_results[1]
            """
            return distance, current_position.attached_cave
        else:
            # Check that the recursive function doesn't exceed the max recursion depth
            if abs(distance) == max_depth:
                # Return a distance of 0, to keep the token stationary
                return 0, 0
            else:
                # Check if the current position has a cave attached
                if current_position.attached_cave and not current_position.attached_cave.occupied:
                    """
                    # Direction True = forwards, direction False = backwards
                    if direction:
                        # Store the results of the search
                        return self.nearest_cave(distance_results, position_results, starting_position, current_position, distance + 1, True,
                                                 direction)
                    else:
                        # Store the results of the search
                        return self.nearest_cave(distance_results, position_results, starting_position, current_position, distance - 1, True,
                                                 direction)
                    """
                    return self.nearest_cave(distance_results, position_results, starting_position, current_position,
                                             distance - 1, True, direction)
                else:
                    """
                    # Continue searching
                    # Direction True = forwards, direction False = backwards
                    if direction:
                        return self.nearest_cave(distance_results, position_results, starting_position, current_position.next_position,
                                                 distance + 1, False, direction)
                    else:
                        return self.nearest_cave(distance_results, position_results, starting_position, current_position.previous_position,
                                                 distance - 1, False, direction)
                    """
                    return self.nearest_cave(distance_results, position_results, starting_position,
                                             current_position.previous_position, distance - 1, False, direction)

    def find_position(self, distance: int):
        if distance > 0:
            position = self.next_position
            for i in range(1, distance):
                position = position.next_position
            return position
        elif distance < 0:
            position = self.previous_position
            for i in range(1, abs(distance)):
                position = position.previous_position
            return position
        else:
            return self

    @abstractmethod
    def load_img(self) -> None:
        pass
