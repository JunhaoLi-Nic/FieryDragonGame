# Imports
from classes.interface.ActionCapable import ActionCapable


class CalculateCard(ActionCapable):
    def __init__(self, card):
        # Inject ChitCard.py dependency through constructor
        self.card = card
        self.position = None

    def set_position(self, position) -> None:
        self.position = position

    def execute(self) -> int:
        # Calculate the intended destination of the flipped card
        return self.card.get_destination(self.position)
