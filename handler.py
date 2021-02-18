from abc import ABC, abstractmethod

import pygame


class PyGameEventMap:

    EXIT = 'exit'
    SHOW_HELP = 'show_help'
    RESET = 'reset'
    KP_PLUS = 'key_plus_down'
    KP_MINUS = 'key_minus_down'
    MOVE_UP = 'move_up'
    MOVE_DOWN = 'move_down'
    MOVE_RIGHT = 'move_right'
    MOVE_LEFT = 'move_left'

    def __init__(self):

        self._keydown_events = {
            pygame.K_ESCAPE:        self.EXIT,
            pygame.K_r:             self.RESET,
            pygame.K_h:             self.SHOW_HELP,
            pygame.K_KP_PLUS:       self.KP_PLUS,
            pygame.K_KP_MINUS:      self.KP_MINUS,
            pygame.K_UP:            self.MOVE_UP,
            pygame.K_DOWN:          self.MOVE_DOWN,
            pygame.K_LEFT:          self.MOVE_LEFT,
            pygame.K_RIGHT:         self.MOVE_RIGHT
        }

        self._event_types = {
            pygame.QUIT:            self.EXIT,
            pygame.KEYDOWN:         self._keydown_events
        }

    def get_event(self, event):
        event_type = self._event_types.get(event.type)
        if event_type is None or isinstance(event_type, str):
            return event_type
        return event_type.get(event.key)


class ABCEventHandler(ABC):

    def __init__(self):
        self._exit = False
        self._pause = True
        self._show_help = False

    def stop(self):
        self._exit = True

    def exit(self):
        self._exit = True

    def show_help(self):
        self._show_help = not self._show_help

    def reset(self):
        pass

    def key_plus_down(self):
        pass

    def key_minus_down(self):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_right(self):
        pass

    def move_left(self):
        pass

    @abstractmethod
    def handle(self, event):
        pass


class PyGameEventHandler(ABCEventHandler):

    def __init__(self):
        super().__init__()
        self._event_map = PyGameEventMap()
        self._event = None

    def handle(self, event):
        method_name = self._event_map.get_event(event)
        if not method_name:
            self._event = None
            return
        method = getattr(self, method_name)
        self._event = event
        method()
        self._event = None

    @property
    def event(self):
        return self._event
