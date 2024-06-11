"""
Class DisplayManager
"""
import pygame
import sys

from classes.concrete.board.Board import Board
from classes.utils.image_packager import resource_path


class DisplayManager:
    screen_size: tuple[int, int]
    game_state: str
    board: Board
    
    def __init__(self, width, height, config) -> None:
        self.screen_size = (width, height)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Fierier Dragons | Sprint 4 | Team 09")
        pygame.display.set_icon(pygame.image.load(resource_path("imgs/APP_ICON.png")))
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.config = config
        
    def get_screen(self) -> pygame.Surface:
        """Get the active screen

        Returns:
            pygame.Surface: The active screen
        """
        return self.screen
    
    def _get_surface(self) -> pygame.Surface:
        """Gets the surface of the display

        Returns:
            pygame.Surface: surface of the display
        """
        return pygame.display.get_surface()

    def draw_setup(self) -> str:
        """Draws the setup screen for the game, where user can choose the number of players

        Returns:
            str: The number of players chosen by the user
        """
        heading_font = pygame.font.Font(None, 48) 
        surface = self._get_surface()

        # Calculate center positions
        screen_width, screen_height = self.screen_size
        checkbox_y_start = screen_height // 2 - 150  # Center the checkboxes vertically
        button_width, button_height = 200, 50
        button_x = screen_width // 2 - button_width // 2
        button_y = checkbox_y_start + 300
        load_button_y = button_y + 100

        # Define checkboxes
        checkboxes = {
            '4 Players': {'rect': pygame.Rect(screen_width // 2 - 100, checkbox_y_start + 100, 20, 20), 'is_checked': False},
            '3 Players': {'rect': pygame.Rect(screen_width // 2 - 100, checkbox_y_start + 125, 20, 20), 'is_checked': False},
            '2 Players': {'rect': pygame.Rect(screen_width // 2 - 100, checkbox_y_start + 150, 20, 20), 'is_checked': False},
            '1 Player': {'rect': pygame.Rect(screen_width // 2 - 100, checkbox_y_start + 175, 20, 20), 'is_checked': False}
        }

        # Automatically check the box based on current configuration
        checkboxes['4 Players']['is_checked'] = True
        checkboxes['3 Players']['is_checked'] = False
        checkboxes['2 Players']['is_checked'] = False
        checkboxes['1 Player']['is_checked'] = False
        
        num_players = 4

        # Define start button
        start_button = pygame.Rect(button_x, button_y, button_width, button_height)

        # Define load game button
        load_button = pygame.Rect(button_x, load_button_y, button_width, button_height)

        # Main loop for the setup screen
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        surface.fill((0, 0, 0))
                        self.config.set_load_save(False)
                        return num_players
                    if load_button.collidepoint(event.pos):
                        surface.fill((0, 0, 0))
                        self.config.set_load_save(True)
                        return num_players
                    for key, value in checkboxes.items():
                        if value['rect'].collidepoint(event.pos):
                            value['is_checked'] = not value['is_checked']
                            for key2, value2 in checkboxes.items():
                                if key2 != key:
                                    value2['is_checked'] = False
                            num_players = int(key[0])

            # Clear the screen and draw elements
            surface.fill((0, 0, 0))
            heading_text = heading_font.render("Setup Game", True, (255, 255, 255))
            surface.blit(heading_text, (screen_width // 2 - heading_text.get_width() // 2, 200))

            # Draw checkboxes and their labels
            for key, value in checkboxes.items():
                pygame.draw.rect(surface, (100, 100, 100) if value['is_checked'] else (255, 255, 255), value['rect'])
                pygame.draw.rect(surface, (255, 255, 255), value['rect'], 2)
                text_surface = self.font.render(key, True, (255, 255, 255))
                surface.blit(text_surface, (value['rect'].x + 35, value['rect'].y-2))

            # Draw the start button
            pygame.draw.rect(surface, (255, 255, 255), start_button)
            pygame.draw.rect(surface, (255, 255, 255), start_button, 2) 
            button_text = self.font.render("Start New Game", True, (0, 0, 0))
            surface.blit(button_text, (start_button.x + button_width // 2 - button_text.get_width() // 2, start_button.y + button_height // 2 - button_text.get_height() // 2))

            # Draw the load button
            pygame.draw.rect(surface, (255, 255, 255), load_button)
            pygame.draw.rect(surface, (255, 255, 255), load_button, 2)
            button_load_text = self.font.render("Load Save Game", True, (0, 0, 0))
            surface.blit(button_load_text, (load_button.x + button_width // 2 - button_load_text.get_width() // 2,
                                       load_button.y + button_height // 2 - button_load_text.get_height() // 2))

            self.update()

        pygame.quit()

    
    def draw_win(self, winner) -> None:
        """
        Displays the winning player colour and offers a reset button

        Args:
            winner (str): The winning player
        Returns:
            None
        """
        surface = self._get_surface()
        
        overlay = pygame.Surface(surface.get_size())
        overlay.fill((0, 0, 0))  
        surface.blit(overlay, (0, 0))

        
        message = self.font.render(f'{winner} wins!', True, (255, 255, 255))
        message_rect = message.get_rect(center=(surface.get_width() // 2, 300))
        surface.blit(message, message_rect)

        self.update()

        button_width, button_height = 200, 50
        reset_button = pygame.Rect((surface.get_width() // 2 - button_width // 2), 500, button_width, button_height)
        button_color = (255, 255, 255)
        text_color = (0, 0, 0)
        corner_radius = 10  
        pygame.draw.rect(surface, button_color, reset_button, border_radius=corner_radius)

        text_surface = self.font.render('RESET', True, text_color)
        text_rect = text_surface.get_rect(center=reset_button.center)

        # Blit the text onto the button
        surface.blit(text_surface, text_rect)

        self.update()

        # Process events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if reset_button.collidepoint(event.pos):
                        self.config.set_load_save(False)
                        return

    
    def update(self) -> None:
        """Update the display
        """
        pygame.display.flip()