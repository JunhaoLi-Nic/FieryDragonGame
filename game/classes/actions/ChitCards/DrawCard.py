# Imports
from classes.interface.ActionCapable import ActionCapable


class DrawCard(ActionCapable):
    def __init__(self, card):
        # Inject ChitCard.py dependency through constructor
        self.card = card

    def execute(self):
        # Flip the associated card
        self.card.flip_card()
