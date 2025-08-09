import sys

import pygame
import json

from src.configs import *
from src.game.event_management import EventHandler
from src.game.state_management import GameState
from src.gui.screen_management import ScreenManager
from src.sounds import SoundManager
from src.log_handle import get_logger
from integracao import IO

logger = get_logger(__name__)

class GameRun:
    def __init__(self):
        logger.info("About to initialize pygame")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Py-Pacman")
        logger.info("pygame initialized")
        self.game_state = GameState()
        logger.info("game state object created")
        self.events = EventHandler(self.screen, self.game_state)
        logger.info("event handler object created")
        self.all_sprites = pygame.sprite.Group()
        self.gui = ScreenManager(self.screen, self.game_state, self.all_sprites)
        logger.info("screen manager object created")
        
        # Inicializar hardware para display de 7 segmentos
        try:
            self.io_device = IO()
            self.last_score = -1  # Para rastrear mudanças no placar
            logger.info("Hardware I/O initialized")
        except Exception as e:
            logger.warning(f"Could not initialize hardware I/O: {e}")
            self.io_device = None

    def initialize_highscore(self):
        with open("levels/stats.json") as fp:
            stats = json.load(fp)
            self.game_state.highscore = stats['highscore']
            self.game_state.mins_played = stats['mins_played']
    
    def create_ghost_mode_event(self):
        CUSTOM_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(CUSTOM_EVENT, 
                              self.game_state.mode_change_events * 1000)
        self.game_state.custom_event = CUSTOM_EVENT

    def initialize_sounds(self):
        sound_manager = SoundManager()
        sound_manager.load_sound("dot", "assets/sounds/pacman_chomp.wav", channel=0)
        sound_manager.load_sound("death","assets/sounds/pacman_death.wav", 0.7, 500, 1)
        sound_manager.load_sound("eat_ghost","assets/sounds/pacman_eatghost.wav", 0.6, 100, 2)
        sound_manager.set_background_music("assets/sounds/backgroud.mp3")
        sound_manager.play_background_music()

    def update_score_display(self):
        """Atualiza o placar no display de 7 segmentos"""
        if self.io_device is None:
            return
            
        current_score = self.game_state.points
        
        # Só atualiza se o placar mudou para evitar writes desnecessários
        if current_score != self.last_score:
            try:
                # Converter pontuação para string e pegar últimos 8 dígitos
                score_str = str(current_score).zfill(8)  # Preenche com zeros à esquerda
                
                # Separar em duas partes de 4 dígitos cada
                # Display direito: últimos 4 dígitos (unidades)
                right_digits = score_str[-4:]
                # Display esquerdo: 4 dígitos anteriores (milhares)  
                left_digits = score_str[-8:-4]
                
                # Atualizar displays
                self.io_device.put_DP(0, right_digits)  # Display direito
                self.io_device.put_DP(1, left_digits)   # Display esquerdo
                
                self.last_score = current_score
                logger.debug(f"Score display updated: {current_score}")
                
            except Exception as e:
                logger.error(f"Error updating score display: {e}")

    def clear_display(self):
        """Limpa o display de 7 segmentos"""
        if self.io_device is None:
            return
        try:
            # Exibir zeros nos displays
            self.io_device.put_DP(0, "0000")  # Display direito
            self.io_device.put_DP(1, "0000")  # Display esquerdo
            logger.info("Display cleared")
        except Exception as e:
            logger.error(f"Error clearing display: {e}")

    def check_highscores(self):
        if self.game_state.points > self.game_state.highscore:
            self.game_state.highscore = self.game_state.points

    def update_highscore(self):
        with open("levels/stats.json", 'w') as fp:
            json.dump({"highscore":self.game_state.highscore,
                       "mins_played": self.game_state.mins_played}, fp, indent=4)
            
    def main(self):
        clock = pygame.time.Clock()
        dt = None
        self.create_ghost_mode_event()
        self.initialize_sounds()
        self.initialize_highscore()
        while self.game_state.running:
            self.events.check_buttons()
            self.game_state.current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                self.events.handle_events(event)
            self.screen.fill(Colors.BLACK)
            self.gui.draw_screens()
            self.all_sprites.draw(self.screen)
            self.all_sprites.update(dt)
            self.check_highscores()
            self.update_score_display()  # Atualizar display de 7 segmentos
            pygame.display.flip()
            dt = clock.tick(self.game_state.fps)
            dt /= 100
        self.update_highscore()
        self.clear_display()  # Limpar display quando o jogo terminar
        pygame.quit()
        sys.exit()
