"""
Class VolcanoCard
"""
import json
from math import floor

from classes.concrete.board.Tile import Tile
from classes.concrete.board.Cave import Cave
from classes.abstract.Position import Position
from classes.enum.Animal import Animal
from classes.enum.Colour import Colour
from classes.utils.file_io import write


class VolcanoCard:
    def __init__(self, tiles: list[Tile], cave: Cave = None):
        self.tiles = tiles
        self.cave = cave

    def get_positions(self) -> list[Position]:
        """returns an ordered list of positions, including cave positions

        Returns:
            list[Position]: list of positions
        """
        positions = []
        for tile in self.tiles:
            positions.append(tile)

        if self.cave:
            # place cave in center of volcano card
            num_of_tiles = len(positions)
            cave_index = floor(num_of_tiles / 2)
            positions[cave_index].attached_cave = self.cave

            # connect cave to tile
            self.cave.next_position = positions[cave_index]

        return positions

    def save(self) -> None:
        """
        saves the current state of the volcano card to a save file
        """
        tiles_arr = []
        for tile in self.tiles:
            tiles_arr.append(tile.animal.value)

        volcano_card = {
            "tiles": tiles_arr
        }

        if self.cave:
            cave = {
                "colour": self.cave.colour.name,
                "animal": self.cave.animal.name,
                "position": 1
            }
            volcano_card["cave"] = cave

        write("VolcanoCards", volcano_card)

    def load(self, save: dict) -> None:
        """
        loads saved state from dict object
        """
        saved_tiles = save["tiles"]
        for i in range(0, len(saved_tiles)):
            save_tile = saved_tiles[i]
            update_tile = self.tiles[i]
            update_tile.animal = Animal[save_tile]
            update_tile.load_img()

        if self.cave:
            saved_cave = save["cave"]
            self.cave.colour = Colour[saved_cave["colour"]]
            self.cave.animal = Animal[saved_cave["animal"]]
            self.cave.load_img()
