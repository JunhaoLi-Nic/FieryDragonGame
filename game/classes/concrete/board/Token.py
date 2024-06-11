"""
Class Token
"""
import pygame.sprite

from classes.abstract.Position import Position
from classes.abstract.GenericSprite import GenericSprite
from classes.concrete.board.Cave import Cave
from classes.concrete.board.Tile import Tile
from classes.enum.Colour import Colour
from classes.utils.image_packager import resource_path


class Token(GenericSprite):
    def __init__(self, coords: tuple[int, int], groups: list[pygame.sprite.Group], colour: Colour, position: Position, starting_cave: Cave):
        super().__init__(coords, groups)
        self.colour = colour
        self.position = position
        self.load_img()
        self.token_active = False
        self.has_won = False
        self.starting_cave = starting_cave
        self.position_before_move = starting_cave
        self.total_moves = 0

    def load_img(self):
        """
        Load the image of the token
        
        :return: None
        """
        self.image = pygame.image.load(self.img_path()).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=self.coords)

    def img_path(self) -> str:
        """
        gets the path of the image

        Returns:
            str: string of the path
        """
        img_path = f"imgs/tokens/{self.colour.name}_TOKEN.png"
        return resource_path(img_path)

    def move_forward(self, moves_left: int):
        """
        Moves the token one position forward

        Args:
            moves_left (int): number of moves left after current move
        Returns:
            None
        Throws:
            Exception: "Invalid move"
        """
        if self.position.attached_cave:
            cave = self.position.attached_cave
            if cave.colour == self.colour and self.total_moves > 1:
                if moves_left == 0:
                    self.move_to_position(cave)
                    self.has_won = True
                    print('Player has won!')
                    return
                else:
                    print("Cannot move beyond cave")
                    raise Exception("Invalid move")

        next_position = self.position.next_position
        if moves_left == 0 and next_position.occupied:
            print("Position is already occupied, cannot move")
            raise Exception("Invalid move")
        self.move_to_position(next_position)

    def move_backward(self, moves_left):
        """
        Moves the token one position back

        Args:
            moves_left (int): number of moves left after current move
        Returns:
            None
        Throws:
            Exception: "Invalid move"
        """
        if isinstance(self.position, Cave):
            if self.position.colour == self.colour:
                print("Cannot move back further than starting cave")
                raise Exception("Invalid move")
        if self.position.attached_cave:
            cave = self.position.attached_cave
            if cave.colour == self.colour:
                if not moves_left:
                    self.move_to_position(cave)
                else:
                    print("Cannot move back further than starting cave")
                    raise Exception("Invalid move")
        previous_position = self.position.previous_position
        if previous_position:
            if moves_left == 0 and previous_position.occupied:
                print("Position is already occupied, cannot move")
                raise Exception("Invalid move")
            self.move_to_position(previous_position)

    def move_to_position(self, new_position: Position):
        """move the token to a new position

        Args:
            new_position (Position): new position to move to
        """
        self.position = new_position
        self.rect = self.image.get_rect(center=self.position.coords)

    def move_token(self, distance: int):
        """move the token a certain distance

        Args:
            distance (int): distance to move
        """
        self.position.occupied = False
        self.position_before_move = self.position
        try:
            moves_left = abs(distance) - 1
            while moves_left >= 0:
                if distance > 0:
                    self.move_forward(moves_left)
                else:
                    self.move_backward(moves_left)
                moves_left -= 1
        except Exception as e:
            self.undo_move()
            raise e

        self.total_moves += distance
        self.position.occupied = True

    def verify_move(self, distance: int, position: Position) -> bool:
        if distance != 0:
            if position.occupied:
                return False
            else:
                return True
        else:
            return False

    def place_token(self, distance: int, position: Position) -> None:
        self.position.occupied = False
        self.position_before_move = self.position
        try:
            self.move_to_position(position)
        except Exception as e:
            self.undo_move()
            raise e
        # Update places moved to accommodate for the shift in board position
        self.total_moves += distance
        self.position.occupied = True


    def undo_move(self):
        """
        Revert's a movements of token if the entire move cannot complete

        Returns:
            None
        """
        self.position = self.position_before_move
        self.position.occupied = True
        self.rect = self.image.get_rect(center=self.position.coords)

    def token_turn(self) -> None:
        """Set the token to active and highlight the starting cave
        """
        self.token_active = True
        self.starting_cave.highlight_cave()

    def token_finish(self) -> None:
        """Set the token to inactive and unhighlight the starting cave
        """
        self.token_active = False
        self.starting_cave.non_highlight_cave()