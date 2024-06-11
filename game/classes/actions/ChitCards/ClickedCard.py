# Imports
from classes.interface.ActionCapable import ActionCapable


class ClickedCard(ActionCapable):
    def __init__(self, card):
        # Inject ChitCard.py dependency through constructor
        self.card = card
        self.mouse_coords = tuple[0, 0]

    def set_mouse_coords(self, mouse_pos: tuple[int, int]) -> None:
        self.mouse_coords = mouse_pos

    def execute(self) -> bool:
        # Calculate the intended destination of the flipped card
        return self.card.card_clicked(self.mouse_coords)
