# Imports
from classes.interface.ActionCapable import ActionCapable


class CheckFlipped(ActionCapable):
    def __init__(self, card):
        # Inject ChitCard.py dependency through constructor
        self.card = card

    def execute(self) -> bool:
        # Calculate the intended destination of the flipped card
        return self.card.get_flipped()
