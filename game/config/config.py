"""
config.py

Author: Liam Nixon
Last modified: 13/05/2024

Contains game configuration settings
"""
from typing import List

class Config:
    # System Variable Default Values
    number_of_players = 4
    number_of_chit_cards = 16
    window_width_px = 800
    window_height_px = 800
    window_full_screen = False
    load_save = False

    # System Constants
    BASE_NUMBER_TILES = number_of_players
    BASE_NUMBER_POSITIONS = 6
    MAX_CHIT_CARD_VALUE = 3

    # Volcano cards
    volcano_cards_with_caves = [
        ["LIZARD", "SPIDER", "BAT"],
        ["SPIDER", "BAT", "LIZARD"],
        ["BAT", "DRAGON", "LIZARD"],
        ["BAT", "SPIDER", "DRAGON"]
    ]

    volcano_cards_without_caves = [
        ["LIZARD", "DRAGON", "SPIDER"],
        ["DRAGON", "LIZARD", "BAT"],
        ["DRAGON", "BAT", "SPIDER"],
        ["SPIDER", "LIZARD", "DRAGON"]
    ]

    # caves
    caves = [
        ["RED", "BAT"],
        ["BLUE", "DRAGON"],
        ["PURPLE", "SPIDER"],
        ["GREEN", "LIZARD"]
    ]

    # chit cards
    standard_chit_cards = [
        {"animal": "LIZARD", "distance": 1, "type": "standard"},
        {"animal": "LIZARD", "distance": 2, "type": "standard"},
        {"animal": "LIZARD", "distance": 3, "type": "standard"},
        {"animal": "DRAGON", "distance": 1, "type": "standard"},
        {"animal": "DRAGON", "distance": 2, "type": "standard"},
        {"animal": "DRAGON", "distance": 3, "type": "standard"},
        {"animal": "SPIDER", "distance": 1, "type": "standard"},
        {"animal": "SPIDER", "distance": 2, "type": "standard"},
        {"animal": "SPIDER", "distance": 3, "type": "standard"},
        {"animal": "BAT", "distance": 1, "type": "standard"},
        {"animal": "BAT", "distance": 2, "type": "standard"},
        {"animal": "BAT", "distance": 3, "type": "standard"},
        {"animal": "PIRATE", "distance": -1, "type": "standard"},
        {"animal": "PIRATE", "distance": -1, "type": "standard"},
        {"animal": "PIRATE", "distance": -2, "type": "standard"},
        {"animal": "PIRATE", "distance": -2, "type": "standard"},
    ]

    special_chit_cards = [
        {"animal": "REVERSE", "type": "reverse"},
        {"animal": "REVERSE", "type": "reverse"},
        {"animal": "REVERSE", "type": "reverse"},
        {"animal": "REVERSE", "type": "reverse"},
    ]

    chit_card_size = 65

    # players
    players = [
        [1, "RED"],
        [2, "BLUE"],
        [3, "PURPLE"],
        [4, "GREEN"]
    ]

    # Configuration Settings Map
    configuration_map = {
        "players": number_of_players,
        "cards": standard_chit_cards,
        "special_cards": special_chit_cards,
        "card_size": chit_card_size,
        "card_max_value": MAX_CHIT_CARD_VALUE,
        "tiles": BASE_NUMBER_TILES,
        "positions": BASE_NUMBER_POSITIONS,
        "window_x": window_width_px,
        "window_y": window_height_px,
        "full_screen": window_full_screen
    }

    
    def __init__(self):
        pass
    
    def set_players(self, num_human_players: int):
        for i in self.players:
            if num_human_players:
                i.append(1)
                num_human_players -= 1
            else:
                i.append(0)
                
    def get_players(self):
        return self.players

    def set_load_save(self, load_save):
        self.load_save = load_save

    def get_load_save(self):
        return self.load_save

    # Configuration Methods
    """
    Returns a list of valid keys for configuration_map.
    Used to validate setting value retrieval.
    """


    def get_valid_keys(self):
        return list(self.configuration_map.keys())


    """
    Returns a value from the configuration map, provided it exists
    """


    def load_config(self, config: str = ""):
        if config in self.configuration_map:
            return self.configuration_map[config]
        else:
            print(
                f"ERROR: {'No config key provided.' if config == '' else f'Config key {config} not found in config_map.'}"
            )
