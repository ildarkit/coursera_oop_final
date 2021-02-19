import os
import random
from abc import ABC, abstractmethod

import pygame

import logic
import service
from objects import Hero
from handler import PyGameEventHandler
from engine import (
    GameSurface, ProgressBar,
    InfoWindow, HelpWindow,
    ScreenHandle
)

SCREEN_DIM = (800, 600)
KEYBOARD_CONTROL = True


class HeroConfig:
    def __init__(self):
        self.base_stats = {
            "strength": 20,
            "endurance": 20,
            "intelligence": 5,
            "luck": 5
        }
        self.path = os.path.join(
            "texture", "Hero.png")


class AbcGame(ABC):

    @abstractmethod
    def create_game(self):
        pass

    @abstractmethod
    def run(self):
        pass


class PyGameHandler(PyGameEventHandler):

    def __init__(self):
        super().__init__()
        pygame.init()
        self.display = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyRPG")

    def event_loop(self):
        for event in pygame.event.get():
            self.handle(event)

    @staticmethod
    def display_update():
        pygame.display.update()

    @staticmethod
    def quit():
        pygame.display.quit()
        pygame.quit()


class Game(PyGameHandler, AbcGame):

    def __init__(self):
        super().__init__()
        self._sprite_size = 60
        self._iteration = 0
        self._hero = None
        self.engine = None
        self.drawer = None
        self.service = None
        self._hero_config = HeroConfig()
        self._hero = None
        self._keyboard_control = KEYBOARD_CONTROL
        self._actions = []

    def init_actions(self):
        if not self._keyboard_control:
            self._actions = [
                self.engine.move_right,
                self.engine.move_left,
                self.engine.move_up,
                self.engine.move_down,
            ]

    def create_game(self):
        self.engine = logic.GameEngine()
        self.service.service_init(self._sprite_size)

        self._hero = Hero(self._hero_config.base_stats,
                          service.create_sprite(self._hero_config.path,
                                                self._sprite_size)
                          )

        self.service.reload_game(self.engine, self._hero)
        self.set_drawer()
        logic.GameEngine.sprite_size = self._sprite_size
        self.drawer.connect_engine(self.engine)
        self.reset_iteration()

    def set_drawer(self):
        handle = ScreenHandle()
        help_handle = HelpWindow((700, 500), pygame.SRCALPHA)
        help_handle.set_successor(handle)
        info = InfoWindow((160, 600))
        info.set_next_coord((50, 50))
        info.set_successor(help_handle)
        progress_bar = ProgressBar((640, 120))
        progress_bar.set_next_coord((640, 0))
        progress_bar.set_successor(info)
        surface = GameSurface((640, 480), pygame.SRCALPHA)
        surface.set_next_coord((0, 480))
        surface.set_successor(progress_bar)
        self.drawer = surface

    def reset_sprite_size(self):
        self.engine.sprite_size = self._sprite_size
        self._hero.sprite = service.create_sprite(
            self._hero_config.path, self._sprite_size
        )
        service.service_init(self._sprite_size, False)

        logic.GameEngine.sprite_size = self._sprite_size
        self.drawer.connect_engine(self.engine)

        self.reset_iteration()

    def reset_iteration(self):
        self._iteration = 0

    def exit(self):
        self.engine.working = False

    def show_help(self):
        self.engine.show_help = not self.engine.show_help

    def key_plus_down(self):
        if not self.is_control_game():
            return
        self._sprite_size += 1
        self.reset_sprite_size()

    def key_minus_down(self):
        if not self.is_control_game():
            return
        self._sprite_size -= 1
        self.reset_sprite_size()

    def reset(self):
        if not self.is_control_game():
            return
        self.create_game()

    def is_game_process(self):
        return self.engine.game_process

    def inc_iteration(self):
        self._iteration += 1

    def move_up(self):
        if not (self.is_control_game() and
                self.is_game_process()):
            return
        self.engine.move_up()
        self.inc_iteration()

    def move_down(self):
        if not (self.is_control_game() and
                self.is_game_process()):
            return
        self.engine.move_down()
        self.inc_iteration()

    def move_left(self):
        if not (self.is_control_game() and
                self.is_game_process()):
            return
        self.engine.move_left()
        self.inc_iteration()

    def move_right(self):
        if not (self.is_control_game() and
                self.is_game_process()):
            return
        self.engine.move_right()
        self.inc_iteration()

    def return_(self):
        if not self.is_control_game() and \
                self.is_game_process():
            return
        self.create_game()

    def is_control_game(self):
        return self._keyboard_control

    def run(self):

        self.init_actions()
        while self.engine.working:
            try:
                self.event_loop()
            except KeyboardInterrupt:
                self.exit()
            except pygame.error as e:
                print(e)
                self.exit()

            if not self.is_control_game():
                if self.engine.game_process:
                    prev_score = self.engine.score
                    self._actions[random.randint(0, 3)]()
                    state = pygame.surfarray.array3d(self.display)
                    reward = self.engine.score - prev_score
                    print(reward)
                else:
                    self.create_game()

            self.display.blit(self.drawer, (0, 0))
            self.drawer.draw(self.display)
            self.display_update()

        self.quit()


if __name__ == '__main__':
    game = Game()
    game.create_game()
    game.run()
