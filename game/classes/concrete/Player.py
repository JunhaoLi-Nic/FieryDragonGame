"""
Class Player
"""

from classes.concrete.board.Token import Token
from classes.utils.file_io import write


class Player:
    def __init__(self, player_number: int, colour: str, token: Token, human: bool):
        self.player_number = player_number
        self.token = token
        self.colour = colour
        self.is_player_turn = False
        self.human = human

    def player_turn(self)-> None:
        self.is_player_turn = True
        self.token.token_turn()

    def player_finish(self)-> None:
        self.is_player_turn = False
        self.token.token_finish()

    def save(self) -> None:
        """
        saves the current state of the player to a save file
        """
        player = {
            "player_num": self.player_number,
            "total_moves": self.token.total_moves,
            "current_player": self.is_player_turn
        }

        write("Players", player)

    def load(self, save: dict) -> None:
        """
        loads the saved state of player
        """
        distance_moved = save["total_moves"]
        position_at = self.token.position.find_position(distance_moved)
        self.token.place_token(distance_moved, position_at)

        if save["current_player"]:
            self.player_turn()
