from pico2d import *

import game_world
from back_ground import BackGround
from basic_monster import BasicMonster
from user_character import UserChar
import game_framework

user_char = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            user_char.handle_event(event)

def init():
    global user_char

    user_char = UserChar()
    game_world.add_object(user_char, 1)

    back_ground = BackGround()
    game_world.add_object(back_ground, 0)

    basic_monster = BasicMonster()
    game_world.add_object(basic_monster, 1)

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass