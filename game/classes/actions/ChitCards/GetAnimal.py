# Imports
from classes.interface.ActionCapable import ActionCapable


class GetAnimal(ActionCapable):
    def __init__(self, card):
        # Inject ChitCard.py dependency through constructor
        self.card = card

    def execute(self):
        # Return the animal associated with the chosen card
        return self.card.animal
