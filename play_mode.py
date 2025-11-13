from random import randint

from pico2d import *


import game_world
from back_ground import BackGround
from basic_monster import BasicMonster
from user_character import UserChar
import game_framework

user_char = None
back_ground = None
basic_monster = None
last_stage = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            user_char.handle_event(event)
            back_ground.handle_event(event)
            basic_monster.handle_event(event)

def init():
    global user_char
    global back_ground
    global basic_monster
    global last_stage

    game_world.enemies.clear()
    game_world.collision_pairs.clear()

    back_ground = BackGround(last_stage)
    game_world.add_object(back_ground, 0)

    uc_x = 0
    uc_y = 400
    basic_x = []
    basic_y = 400
    basic_num = 0

    if back_ground.stage_num == 1:
        uc_x = 300
        uc_y = 400
        basic_x.append(randint(1300, 1600))
        basic_y = 400
        basic_num = 1
    elif back_ground.stage_num == 2:
        uc_x = 960
        uc_y = 400
        basic_x.append(randint(1300, 1600))
        basic_x.append(randint(1600, 1900))
        basic_x.append(randint(300, 600))
        basic_y = 400
        basic_num = 3
    elif back_ground.stage_num == 3:
        uc_x = 300
        uc_y = 400

    user_char = UserChar(uc_x, uc_y)
    game_world.add_object(user_char, 1)

    basic_monsters = [BasicMonster(basic_x[i], basic_y, user_char) for i in range(basic_num)]
    game_world.add_objects(basic_monsters, 1)
    for basic_monster in basic_monsters:
        game_world.enemies.add(basic_monster)

    game_world.add_collision_pair('uc:fire', user_char, None)
    for basic_monster in basic_monsters:
        game_world.add_collision_pair('basic:bullet', basic_monster, None)

    if back_ground:
        last_stage = back_ground.stage_num


def update():
    global last_stage

    game_world.update()
    game_world.handle_collisions()

    if back_ground:
        if last_stage != back_ground.stage_num:
            finish()
            init()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass