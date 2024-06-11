from sys import exit
from time import sleep

import pygame

from classes.concrete.board.Board import Board
from classes.utils.image_packager import resource_path
from config.config import Config
from classes.concrete.rendering.DisplayManager import DisplayManager

pygame.init()

def setup():
    config = Config()
    display = DisplayManager(config.window_width_px, config.window_height_px, config)
    clock = pygame.time.Clock()
    config.set_players(display.draw_setup())
    board = Board(display.screen_size[0], display.screen_size[1], config)
    return display, config, board

def main():
    # game loop
    display, config, board = setup()
    while True:
        for event in pygame.event.get():
            # quit the game if user exits the window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                board.handle_click(mouse_pos)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     winning_player = 'red'
            #     display.draw_win(winning_player)
            #     setup()
        board.draw(display.get_screen())
        pygame.display.update()
        
        if not board.current_player.human and not board.card_flip_timer.active:
            board.draw(display.get_screen())
            pygame.display.update()
            sleep(2)
            board.handle_non_human_turn()
            
        if board.player_has_won():
            winner = board.get_winner()
            display.draw_win(winner)
            main()
            
if __name__ == "__main__":
    main()  
