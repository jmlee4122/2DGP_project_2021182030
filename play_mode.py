from random import randint

from pico2d import *

import clear_menu_mode
import game_world
import menu_mode
from back_ground import BackGround
from basic_monster import BasicMonster
from boss_monster import BossMonster
from user_character import UserChar
import game_framework

user_char = None
back_ground = None
basic_monster = None
boss_monster = None
last_stage = None

saved_user_char = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(menu_mode)
        else:
            if user_char is not None:
                user_char.handle_event(event)
            if back_ground is not None:
                back_ground.handle_event(event)
            if basic_monster is not None:
                basic_monster.handle_event(event)
            if boss_monster is not None:
                boss_monster.handle_event(event)

def init():
    global user_char
    global back_ground
    global basic_monster
    global boss_monster
    global last_stage

    global saved_user_char

    game_world.enemies.clear()
    game_world.collision_pairs.clear()

    back_ground = BackGround(last_stage)
    game_world.add_object(back_ground, 0)

    uc_x = 0
    uc_y = 400

    basic_x = []
    basic_y = 400
    basic_num = 0

    boss_x = 0
    boss_y = 400
    boss_num = 0

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
        basic_x.append(randint(1300, 1600))
        basic_x.append(randint(300, 600))
        basic_y = 400
        basic_num = 3
    elif back_ground.stage_num == 3:
        uc_x = 300
        uc_y = 400
        boss_x = 1500
        boss_y = 400
        boss_num = 1

    if saved_user_char == None:
        user_char = UserChar(uc_x, uc_y)
    else:
        user_char = saved_user_char
        user_char.x = uc_x
        user_char.y = uc_y
    game_world.add_object(user_char, 1)

    if back_ground.stage_num == 1 or back_ground.stage_num == 2:
        basic_monsters = [BasicMonster(basic_x[i], basic_y, user_char) for i in range(basic_num)]
        game_world.add_objects(basic_monsters, 1)
        for basic_monster in basic_monsters:
            game_world.enemies.add(basic_monster)
    elif back_ground.stage_num == 3:
        boss_monsters = [BossMonster(boss_x, boss_y, user_char) for i in range(boss_num)]
        game_world.add_objects(boss_monsters, 1)
        for boss_monster in boss_monsters:
            game_world.enemies.add(boss_monster)



    game_world.add_collision_pair('uc:fire', user_char, None)
    game_world.add_collision_pair('uc:slash', user_char, None)
    if back_ground.stage_num == 1 or back_ground.stage_num == 2:
        for basic_monster in basic_monsters:
            game_world.add_collision_pair('basic:bullet', basic_monster, None)
    elif back_ground.stage_num == 3:
        for boss_monster in boss_monsters:
            game_world.add_collision_pair('boss:bullet', boss_monster, None)

    if back_ground:
        last_stage = back_ground.stage_num


def update():
    global last_stage
    global user_char
    global saved_user_char

    game_world.update()
    game_world.handle_collisions()

    if back_ground:
        if last_stage != back_ground.stage_num:
            if last_stage == 3:
                # print("Boss Stage Clear!")
                # delay(0.5)
                # game_framework.push_mode(clear_menu_mode)
                return
            saved_user_char = user_char
            finish()
            init()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    #global last_stage
    #last_stage = 0
    game_world.clear()

def pause(): pass
def resume(): pass