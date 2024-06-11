# Imports
from classes.interface.ActionCapable import ActionCapable


class ResetCard(ActionCapable):
    def __init__(self, card):
        # Inject ChitCard.py dependency through constructor
        self.card = card

    def execute(self):
        # Reset the associated card
        self.card.reset_card()
