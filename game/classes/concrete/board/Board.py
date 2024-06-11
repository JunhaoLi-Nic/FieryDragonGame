"""
Class Board
"""
import math
import random

import pygame
from random import randrange, choice

from classes.abstract.GenericSprite import GenericSprite
from classes.concrete.board.Cave import Cave
from classes.concrete.board.Tile import Tile
from classes.concrete.board.VolcanoCard import VolcanoCard
from classes.concrete.Player import Player
from classes.concrete.board.Token import Token
from classes.enum.Animal import Animal
from classes.enum.Colour import Colour
from classes.utils.file_io import load_file, delete_save, write
from classes.utils.image_packager import resource_path
from classes.utils.timer import Timer
from config.config import Config

from classes.actions.ChitCards.Invokers.ChitCardInvoker import ChitCardInvoker
from classes.abstract.ChitCard import ChitCard
from classes.concrete.board.StandardCard import StandardCard
from classes.concrete.board.ReverseCard import ReverseCard


class Board:
    def __init__(self, width: int, height: int, config: Config) -> None:

        self.width = width
        self.height = height
        self.config = config

        # parameters for circular board track
        self.center = (self.width / 2, self.height / 2)
        self.track_width = 80
        self.radius = self.height / 2 - self.track_width

        # parameters for chit pool
        self.grid = 5
        self.offset = 4.1

        # sprite groups
        self.tile_sprite_group = pygame.sprite.Group()
        self.cave_sprite_group = pygame.sprite.Group()
        self.token_sprite_group = pygame.sprite.Group()
        self.chit_sprite_group = pygame.sprite.Group()
        self.ui_sprite_group = pygame.sprite.Group()

        # tracked board components
        self.volcano_cards = self.generate_volcano_cards()
        self.caves = self.generate_caves()
        self.chit_cards = self.generate_chit_cards()
        self.connect_board()
        self.players = self.generate_players()
        self.current_player = self.players[1]
        self.current_player.player_turn()
        self.last_flipped_chit = None

        # timers
        self.card_flip_timer = Timer(1500, self.card_flipped)

        # font
        self.font = pygame.font.Font(None, 36)

        # Initialize button properties
        self.button_width, self.button_height = 550, 50
        self.button_x, self.button_y = 25, self.height - self.button_height - 10  # 10 pixels from the bottom and left edges
        self.button_surface = pygame.Surface((self.button_width, self.button_height))
        self.button_surface.fill('black')
        self.font = pygame.font.Font(None, 36)  # Ensure the font is initialized here
        button_text = self.font.render('Memory Score', True, 'white')
        self.button_surface.blit(button_text, button_text.get_rect(bottomleft=(0, 25)))

        self.previous_turn = self.current_player
        self.max_score = [0, self.current_player]  # init for player
        self.num_flips = 0

        # load saved game
        self.load_save()

        # debugging setup
        # self.current_player.token.move_token(6)
        # self.players[2].token.move_token(1)
        # self.players[3].token.move_token(10)

    def generate_volcano_cards(self) -> list[VolcanoCard]:
        """generate volcano cards for the board

        Returns:
            list[VolcanoCard]: a list of volcano cards
        """
        num_tiles = self.calculate_num_tiles()
        tile_coordinates = self.find_points_on_circle(num_tiles, self.radius - self.track_width / 2, self.center)
        # move the last coordinate to index 0, so that volcano cards are arranged correctly
        tile_coordinates.insert(0, tile_coordinates.pop(-1))

        cards_with_caves = self.config.volcano_cards_with_caves.copy()
        cards_without_caves = self.config.volcano_cards_without_caves.copy()

        volcano_cards = []

        for i in range(0, len(self.config.volcano_cards_with_caves)):
            # alternate volcano cards with caves and without caves to build board in correct order
            random_card_with_cave = cards_with_caves.pop(randrange(len(cards_with_caves)))
            card1_tiles = []
            for animal in random_card_with_cave:
                card1_tiles.append(Tile(tile_coordinates.pop(0), [self.tile_sprite_group], Animal[animal]))
            volcano_cards.append(VolcanoCard(card1_tiles))

            random_card_without_cave = cards_without_caves.pop(randrange(len(cards_without_caves)))
            card2_tiles = []
            for animal in random_card_without_cave:
                card2_tiles.append(Tile(tile_coordinates.pop(0), [self.tile_sprite_group], Animal[animal]))
            volcano_cards.append(VolcanoCard(card2_tiles))

        return volcano_cards

    # Generates list of caves from self.config
    def generate_caves(self) -> dict[Colour: Cave]:
        # place caves across 4 corners attached to volcano cards with cave indents
        # assumes volcano_cards all have the same number of tiles
        cave_coords = self.find_points_on_circle(self.config.number_of_players,
                                                 self.radius + self.track_width / 2 - 10, self.center)

        # to find the correct volcano cards to add caves to
        volcano_card_indexes = []
        match self.config.number_of_players:
            case 2:
                volcano_card_indexes = [0, 4]
            case 3:
                volcano_card_indexes = [0, 2, 4]
            case 4:
                volcano_card_indexes = [0, 2, 4, 6]

        # create cave and add to volcano card
        caves = self.config.caves.copy()

        cave_dict = {}
        for i in range(0, len(volcano_card_indexes)):
            cave_colour = caves[i][0]
            cave_animal = caves[i][1]
            cave = Cave(cave_coords[i], [self.cave_sprite_group], Animal[cave_animal], Colour[cave_colour])
            self.volcano_cards[volcano_card_indexes[i]].cave = cave
            cave_dict.update({cave_colour: cave})
        return cave_dict

    def generate_single_card(self, position: int, row: int, offset: float, data: dict[str, any]) -> ChitCard | None:
        chit = None
        # Determine which card to instantiate from passed data
        match data["type"]:
            case "standard":
                # Instantiate a new StandardCard from the data
                chit = StandardCard(
                    self.config.load_config('card_size'),
                    (position + offset, row + offset),
                    [self.chit_sprite_group],
                    Animal[data["animal"]],
                    data["distance"]
                )
            case "reverse":
                # Instantiate a new ReverseCard from the data
                chit = ReverseCard(
                    self.config.load_config('card_size'),
                    (position + offset, row + offset),
                    [self.chit_sprite_group],
                    Animal[data["animal"]]
                )
            # Catch case:
            case _:
                # Create a standard card from the data
                print(f'Error: {type} does not match known chit card types, returning None')
        return chit

    def generate_chit_cards(self) -> list[ChitCardInvoker] | None:
        # moves grid of chit cards to centre of board
        chits = []
        standard_chit_cards = self.config.load_config('cards')
        special_chit_cards = self.config.load_config('special_cards')
        # Define a max width for the grid
        # Track the current placement of the chit card on the grid
        current_position = 0
        # Track the current grid row
        current_row = 0
        while len(standard_chit_cards) > 0 or len(special_chit_cards) > 0:
            # Calculate chit coordinates
            if current_position == self.grid:
                current_position = 0
                current_row += 1
            if len(standard_chit_cards) > 0 and len(special_chit_cards) > 0:
                # Extract the chit card's data
                card_type = random.choice(
                    [
                        standard_chit_cards,
                        special_chit_cards
                    ])
                chit_data = card_type.pop(randrange(len(card_type)))
            elif len(standard_chit_cards) > 0:
                # Extract the chit card's data
                chit_data = standard_chit_cards.pop(randrange(len(standard_chit_cards)))
            else:
                # Extract the chit card's data
                chit_data = special_chit_cards.pop(randrange(len(special_chit_cards)))

            # Generate a card based on the extracted data
            chit = self.generate_single_card(current_position, current_row, self.offset, chit_data)
            if chit:
                # Configure the invoker class
                controller = ChitCardInvoker(chit)
                # Store the invoker
                chits.append(controller)
                # Increment the position in the grid
                current_position += 1
            else:
                # If there is an error creating chit cards, cancel the process and return a blank list
                return None
        return chits

    def generate_players(self) -> dict[int: Player]:
        """
        Generate players for the game

        Returns:
            list[Player]: a list of Players
        """
        players = {}
        for i in self.config.get_players():
            player = i
            number = player[0]
            colour = player[1]
            cave = self.caves[colour]
            human = bool(player[2])
            token = Token(self.caves[colour].coords, [self.token_sprite_group], Colour[colour], cave, cave)
            players.update({player[0]: Player(number, colour, token, human)})
        return players

    def connect_board(self):
        # set previous position for all positions on board
        previous_position = None
        for volcano_card in self.volcano_cards:
            for position in volcano_card.get_positions():
                position.previous_position = previous_position
                previous_position = position
        # set previous position for first position to be the final position to close the circle
        self.volcano_cards[0].get_positions()[0].previous_position = previous_position

        # set next position for all positions on the board
        for volcano_card in self.volcano_cards:
            for position in volcano_card.get_positions():
                position.previous_position.next_position = position

        # print statements useful for debugging
        '''
        for volcano_card in self.volcano_cards:
            for position in volcano_card.get_positions():
                previous_position = position.previous_position
                print(previous_position.__class__.__name__ + ': ' + previous_position.animal.value)
                print('^')

        print('======================')
        for volcano_card in self.volcano_cards:
            if volcano_card.cave:
                print(volcano_card.cave.next_position.animal)

            for position in volcano_card.get_positions():
                next_position = position.next_position
                print('Next pos = ' + next_position.__class__.__name__ + ': ' + next_position.animal.value)
                print('V')
        '''

    # Calculate total num of tiles from self.config
    def calculate_num_tiles(self) -> int:
        num_tiles = 0
        for volcano_card in self.config.volcano_cards_with_caves:
            num_tiles += len(volcano_card)
        for volcano_card in self.config.volcano_cards_without_caves:
            num_tiles += len(volcano_card)
        return num_tiles

    # finds equally distanced points around a circle radius
    @staticmethod
    def find_points_on_circle(num_points: int, radius: float, center: tuple) -> list:
        list_of_points = []
        board_slice = 2 * math.pi / num_points
        for i in range(num_points):
            angle = board_slice * i
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            list_of_points.append((x, y))
        return list_of_points

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the current state of the board to the display
        Args:
            surface (pygame.Surface): The surface to draw the board to
        Returns:
            None
        """
        pygame.draw.circle(
            surface=surface,
            color='white',
            center=self.center,
            radius=self.radius,
            width=self.track_width)

        # display current player
        text_surface = pygame.Surface((300, 80))
        text_surface.fill('black')
        surface.blit(text_surface, text_surface.get_rect(topleft=(0, 0)))
        if self.current_player.human:
            message = self.font.render(f"{self.current_player.token.colour.value} player's turn", True,
                                    (255, 255, 255))
        else:
            message = self.font.render(f"{self.current_player.token.colour.value} (CPU) player's turn", True,
                                    (255, 255, 255))
        message_rect = message.get_rect(topleft=(25, 25))
        surface.blit(message, message_rect)

        # display animal of current position
        current_animal = pygame.Surface((250, 80))
        current_animal.fill('black')
        text = self.font.render('token is on', True, 'white')
        current_animal.blit(text, text.get_rect(topleft=(0, 30)))
        animal = pygame.image.load(self.current_player.token.position.animal_img_path()).convert_alpha()
        animal = pygame.transform.scale(animal, (80, 80))
        current_animal.blit(animal, animal.get_rect(center=(180, 40)))
        surface.blit(current_animal, current_animal.get_rect(topright=(800, 0)))

        # Draw the button
        surface.blit(self.button_surface, (self.button_x, self.button_y))

        # display save game button
        self.save_button = GenericSprite((780, 780), [self.ui_sprite_group])
        self.save_button.image = pygame.image.load(resource_path("imgs/save.png")).convert_alpha()
        self.save_button.image = pygame.transform.scale(self.save_button.image, (80, 80))
        self.save_button.rect = self.save_button.image.get_rect(bottomright=self.save_button.coords)

        # # display load game button
        # self.load_button = GenericSprite((20, 780), [self.ui_sprite_group])
        # self.load_button.image = pygame.image.load("imgs/save.png").convert_alpha()
        # self.load_button.image = pygame.transform.scale(self.load_button.image, (80, 80))
        # self.load_button.rect = self.load_button.image.get_rect(bottomleft=self.load_button.coords)


        # draw all sprites to surface
        self.tile_sprite_group.draw(surface)
        self.cave_sprite_group.draw(surface)
        self.token_sprite_group.draw(surface)
        self.chit_sprite_group.draw(surface)
        self.ui_sprite_group.draw(surface)
        self.card_flip_timer.update()
        self.cave_sprite_group.update()

    # Function to display the popup window
    def show_popup(self, surface: pygame.Surface):
        popup_width, popup_height = 300, 150
        popup_x, popup_y = (self.width - popup_width) // 2, (self.height - popup_height) // 2
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill('gray')

        # Define the text to display
        text_lines = [
            "Best Memory Score: " f"{self.max_score[0]}",
            "Best Memory Player:",
            f"{self.max_score[1].token.colour.value}" " Player"
        ]

        # Render each line of text
        line_height = 30  # Height of each line
        for i, line in enumerate(text_lines):
            popup_text = self.font.render(line, True, 'black')
            text_rect = popup_text.get_rect(center=(popup_width // 2, 50 + i * line_height))
            popup_surface.blit(popup_text, text_rect)

        surface.blit(popup_surface, (popup_x, popup_y))
        pygame.display.update()
        pygame.time.wait(2000)  # Display the popup for 2 seconds

    def handle_click(self, mouse_pos):
        """
        Handles input coming from the game loop

        Args:
            mouse_pos (tuple[int, int]): the x and y coordinates of the mouse when it was clicked
        Returns:
            None
        """
        if self.save_button.rect.collidepoint(mouse_pos):
            self.save()

        # if self.load_button.rect.collidepoint(mouse_pos):
        #     self.load_save()

        if self.button_x <= mouse_pos[0] <= self.button_x + self.button_width and \
                self.button_y <= mouse_pos[1] <= self.button_y + self.button_height:
            self.show_popup(pygame.display.get_surface())

        if not self.card_flip_timer.active:
            for chit in self.chit_cards:
                if chit.card_clicked(mouse_pos) and not chit.card_flipped():
                    chit.draw_card()
                    self.last_flipped_chit = chit
                    self.card_flip_timer.activate()

    def handle_non_human_turn(self):
        current_player = self.current_player
        chits = [chit for chit in self.chit_cards if not chit.card_flipped()]
        chit = randrange(len(chits))
        chits[chit].card_clicked(cpu=True)
        chits[chit].draw_card()
        self.last_flipped_chit = chits[chit]
        self.card_flip_timer.activate()
        

    def card_flipped(self):
        """
        Moves player token appropriate based on chit card and end's turn if wrong animal on chit card

        Returns:
            None
        """
        if self.last_flipped_chit:
            chit = self.last_flipped_chit
            if chit.get_card_animal() in [self.current_player.token.position.animal, Animal["PIRATE"]]:
                try:
                    self.current_player.token.move_token(chit.get_destination())
                    if self.current_player == self.previous_turn:
                        self.num_flips += 1
                    if self.num_flips > self.max_score[0]:
                        self.max_score[0] = self.num_flips
                        self.max_score[1] = self.current_player

                except Exception as e:
                    self.next_player()
            elif chit.get_card_animal() == Animal["REVERSE"]:
                distance, destination = chit.get_destination(self.current_player.token.position)
                valid = self.current_player.token.verify_move(distance, destination)
                if valid:
                    self.current_player.token.place_token(distance, destination)
                    # self.next_player()
            else:
                self.next_player()

    def next_player(self) -> None:
        """
        Starts the next player's turn

        Returns:
            None
        """
        for chit in self.chit_cards:
            chit.reset_card()


        self.num_flips = 0
        self.current_player.player_finish()
        current_player_number = self.current_player.player_number
        # Set previous player's turn to false
        if current_player_number == self.config.number_of_players:
            next_player_number = 1
        else:
            next_player_number = current_player_number + 1
        self.current_player = self.players[next_player_number]
        # flag for player's turn start so that it trigger the cave
        self.current_player.player_turn()
        self.previous_turn = self.current_player

    def player_has_won(self) -> bool:
        """
        Check's if any player has won

        Returns:
            bool
        """
        for player in self.players.values():
            if player.token.has_won:
                return True

    def get_winner(self) -> str:
        """
        Gets the game winner

        Returns:
            winning player number as a string
        """
        for player in self.players.values():
            if player.token.has_won:
                return str(player.player_number)

    def save(self) -> None:
        # delete current save to write new save file
        delete_save()

        for volcano_card in self.volcano_cards:
            volcano_card.save()

        for chit_card in self.chit_cards:
            chit_card.save()

        for player in self.players.values():
            player.save()

        # save memory score
        memory_score = {
            "score": self.max_score[0],
            "player": self.max_score[1].player_number
        }
        write("MemoryScore", memory_score)

        saved_text = self.font.render("Game saved!", True, (255, 255, 255))
        pygame.display.get_surface().blit(saved_text, (630, 670))
        pygame.display.update()
        pygame.time.wait(2000)
        saved_text.fill((0, 0, 0))
        pygame.display.get_surface().blit(saved_text, (630, 670))
        pygame.display.update()

    def load_save(self) -> None:
        """
        loads the saved state of the game into the board
        """
        if self.config.get_load_save():
            save = load_file()
            if save:
                # load volcano cards
                saved_volcano_cards = save["VolcanoCards"]
                for i in range(0, len(self.volcano_cards)):
                    volcano_card = self.volcano_cards[i]
                    saved_volcano_card = saved_volcano_cards[i]
                    volcano_card.load(saved_volcano_card)

                # load players
                saved_players = save["Players"]
                for saved_player in saved_players:
                    player_num = saved_player["player_num"]
                    player = self.players[player_num]
                    player.load(saved_player)
                    if saved_player["current_player"]:
                        self.current_player.player_finish()
                        self.current_player = self.players[player_num]

                # load chit cards
                saved_chit_cards = save["ChitCards"]
                current_position = 0
                current_row = 0
                for i in range(0, len(self.chit_cards)):
                    if current_position == self.grid:
                        current_position = 0
                        current_row += 1
                    self.chit_cards[i].load(self.generate_single_card(current_position, current_row, self.offset, saved_chit_cards[i]))
                    current_position += 1

                # load memory score
                memory_score = save["MemoryScore"][0]
                self.max_score[0] = memory_score["score"]
                self.max_score[1] = self.players[memory_score["player"]]
