# Imports
from classes.interface.ActionCapable import ActionCapable


class LoadCard(ActionCapable):
    def __init__(self, card):
        # Inject ChitCard.py dependency through constructor
        self.card = card

    def execute(self) -> int:
        # Calculate the intended destination of the flipped card
        return self.card.load()
