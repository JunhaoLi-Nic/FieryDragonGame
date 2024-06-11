# Imports
from classes.interface.ActionCapable import ActionCapable
from classes.actions.ChitCards.DrawCard import DrawCard
from classes.actions.ChitCards.ResetCard import ResetCard
from classes.actions.ChitCards.CalculateCard import CalculateCard
from classes.actions.ChitCards.ClickedCard import ClickedCard
from classes.actions.ChitCards.CheckFlipped import CheckFlipped
from classes.actions.ChitCards.GetAnimal import GetAnimal
from classes.actions.ChitCards.SaveCard import SaveCard
from classes.actions.ChitCards.CPUClickedCard import CPUClickedCard


class ChitCardInvoker:
    def __init__(self, card):
        # Initially set to None, to ensure proper configuration before use
        self._draw_action = DrawCard(card)
        self._reset_action = ResetCard(card)
        self._get_destination = CalculateCard(card)
        self._card_clicked = ClickedCard(card)
        self._cpu_card_clicked = CPUClickedCard(card)
        self._card_flipped = CheckFlipped(card)
        self._get_card_animal = GetAnimal(card)
        self._save_action = SaveCard(card)

    def draw_card(self):
        """
        Invokes the flip_card() method on ChitCard.py by invoking it through the DrawCard.py command object
        :return: None
        """
        self._draw_action.execute()

    def reset_card(self):
        """
        Invokes the reset_card() method on ChitCard.py by invoking it through the DrawCard.py command object
        :return: None
        """
        self._reset_action.execute()

    def get_destination(self, position = None) -> int:
        """
        Invokes the get_destination() method on ChitCard.py by invoking it through the CalculateCard.py command object
        :return: None
        """
        self._get_destination.set_position(position)
        return self._get_destination.execute()

    def card_clicked(self, mouse_pos: tuple[int, int]=None, cpu=False) -> bool:
        """
        Invokes the card_clicked() method on ChitCard.py by invoking it through the CardClicked.py command object
        :return: bool
        """
        if mouse_pos and not cpu:
            self._card_clicked.set_mouse_coords(mouse_pos)
        elif not mouse_pos and not cpu:
            raise ValueError("Mouse position required for human player")
        
        return self._card_clicked.execute()

    def card_flipped(self) -> bool:
        """
        Invokes the card_flipped() method on ChitCard.py by invoking it through the CheckFlipped.py command object
        :return: bool
        """
        return self._card_flipped.execute()

    def get_card_animal(self):
        """
        Gets a reference to the animal property on ChitCard.py by invoking it through the GetAnimal.py command object
        :return: Animal
        """
        return self._get_card_animal.execute()

    def save(self):
        self._save_action.execute()

    def load(self, card):
        self._draw_action = DrawCard(card)
        self._reset_action = ResetCard(card)
        self._get_destination = CalculateCard(card)
        self._card_clicked = ClickedCard(card)
        self._cpu_card_clicked = CPUClickedCard(card)
        self._card_flipped = CheckFlipped(card)
        self._get_card_animal = GetAnimal(card)
        self._save_action = SaveCard(card)
