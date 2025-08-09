from pygame import (QUIT, K_q)
from pygame import USEREVENT
from pygame.time import set_timer
from integracao import *

io = IO()

class EventHandler:
    def __init__(self, screen, game_state):
        self._screen = screen
        self._game_screen = game_state
        self.io = IO()

    def pygame_quit(self):
        self._game_screen.running = False

    def check_buttons(self):
    	if io.get_PB(1) == 0:
        	self._game_screen.direction = "l"
    	elif io.get_PB(0) == 0:
        	self._game_screen.direction = "r"
    	elif io.get_PB(3) == 0:
        	self._game_screen.direction = "u"
    	elif io.get_PB(2) == 0:
        	self._game_screen.direction = "d"

    def handle_events(self, event):
        if event.type == QUIT:
            self.pygame_quit()
        
        if event.type == self._game_screen.custom_event:
            curr_mode = self._game_screen.ghost_mode
            if curr_mode == 'scatter':
                self._game_screen.ghost_mode = 'chase'
            elif curr_mode == 'chase':
                self._game_screen.ghost_mode = 'scatter'
            CUSTOM_EVENT = USEREVENT + 1
            set_timer(CUSTOM_EVENT, 
                                self._game_screen.mode_change_events * 1000)
            self._game_screen.custom_event = CUSTOM_EVENT
        
        if event.type == self._game_screen.power_up_event:
            self._game_screen.is_pacman_powered=False
	

