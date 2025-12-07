from pico2d import load_image, draw_rectangle, get_time, load_font, delay
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_SPACE, SDLK_DOWN, SDLK_q

import clear_menu_mode
import game_framework
import game_world
from bullet import Bullet
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def hp_depleted(e):
    return e[0] == 'HP' and e[1] == 'DEATH'
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q
def q_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_q


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION_DEATH = 1.0
ACTION_PER_TIME_DEATH = 1.0 / TIME_PER_ACTION_DEATH
FRAMES_PER_ACTION_DEATH = 8

TIME_PER_ACTION_JUMP = 0.3
ACTION_PER_TIME_JUMP = 1.0 / TIME_PER_ACTION_JUMP
FRAMES_PER_ACTION_JUMP = 6
GRAVITY = 9.8  # 중력 가속도 (m/s²)

TIME_PER_ACTION_RUN = 0.3
ACTION_PER_TIME_RUN = 1.0 / TIME_PER_ACTION_RUN
FRAMES_PER_ACTION_RUN = 6

# 공격 이미지를 유지할 시간 (프레임레이트에 맞게 조절)
ATTACK_DURATION = 0.05  # 초


class DefendIdle:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_defend.png')

    def enter(self, e):
        self.uc.is_defending = True
        self.uc.frame = 0

    def exit(self, e):
        self.uc.is_defending = False

    def do(self):
        pass

    def draw(self):
        if self.uc.face_dir == 1:
            self.image.draw(self.uc.x, self.uc.y, 402, 382)
        else:
            self.image.composite_draw(0, 'h', self.uc.x, self.uc.y, 402, 382)

class DefendRun:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_defend.png')

    def enter(self, e):
        self.uc.is_defending = True
        self.uc.frame = 0
        if q_down(e): # run -> defend run
            pass
        else: # defend idle -> defend run
            if right_down(e) or left_up(e):
                self.uc.delta_move = self.uc.face_dir = 1
            elif left_down(e) or right_up(e):
                self.uc.delta_move = self.uc.face_dir = -1

    def exit(self, e):
        self.uc.is_defending = False

    def do(self):
        pass

    def draw(self):
        if self.uc.face_dir == 1:
            self.image.draw(self.uc.x, self.uc.y, 402, 382)
        else:
            self.image.composite_draw(0, 'h', self.uc.x, self.uc.y, 402, 382)

class Death:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_death_sprite_sheet.png')
        self.clip_width = 402
        self.clip_height = 382
        self.finished = False

    def enter(self, e):
        self.uc.frame = 0
        self.uc.is_moving = False
        self.uc.y = 400
        self.finished = False

    def exit(self, e):
        pass

    def do(self):
        dt = min(game_framework.frame_time, 0.06)
        if not self.finished:
            self.uc.frame = (self.uc.frame + FRAMES_PER_ACTION_DEATH * ACTION_PER_TIME_DEATH * dt) % 8
            if int(self.uc.frame) == 7:
                self.finished = True
        else:
            self.uc.is_dead = True
            delay(1.0)
            game_framework.push_mode(clear_menu_mode)

    def draw(self):
        if self.uc.face_dir == 1:
            self.image.clip_draw(
                int(self.uc.frame - 1) * self.clip_width, 0, self.clip_width, self.clip_height,
                self.uc.x, self.uc.y, 300, 300
            )
        else:
            self.image.clip_composite_draw(
                int(self.uc.frame - 1) * self.clip_width, 0, self.clip_width, self.clip_height,
                0, 'h', self.uc.x, self.uc.y, 300, 300
            )

class DownRun:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_r_down.png')

    def enter(self, e):
        self.uc.is_down = True
        if down_down(e): # run -> down run
            pass
        else: # down idle -> down run
            if right_down(e) or left_up(e):
                self.uc.delta_move = self.uc.face_dir = 1
            elif left_down(e) or right_up(e):
                self.uc.delta_move = self.uc.face_dir = -1
        file_path = '2DGP_character/user_character/'
        if self.uc.face_dir == 1:
            self.image = load_image(file_path + 'user_r_down.png')
        else:
            self.image = load_image(file_path + 'user_l_down.png')

    def exit(self, e):
        self.uc.is_down = False

    def do(self):
        pass

    def draw(self):
        self.image.draw(self.uc.x, self.uc.y)

class DownIdle:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_r_down.png')

    def enter(self, e):
        self.uc.is_down = True
        self.uc.delta_move = 0
        file_path = '2DGP_character/user_character/'
        if self.uc.face_dir == 1:
            self.image = load_image(file_path + 'user_r_down.png')
        else:
            self.image = load_image(file_path + 'user_l_down.png')

    def exit(self, e):
        self.uc.is_down = False

    def do(self):
        pass

    def draw(self):
        self.image.draw(self.uc.x, self.uc.y)

class Run:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_running_sprite_sheet.png')
        file_path = '2DGP_attack/'
        self.attack_image_R = load_image(file_path + 'uc_attack_R.png')
        self.attack_image_L = load_image(file_path + 'uc_attack_L.png')
        self.clip_width = 402
        self.clip_height = 382
        self.clip_bottom = 0

    def enter(self, e):
        self.uc.frame = 0
        self.uc.is_moving = True

        if down_up(e):
            if self.uc.face_dir == 1:
                self.clip_bottom = 0
            elif self.uc.face_dir == -1:
                self.clip_bottom = 2
        elif q_up(e):
            if self.uc.face_dir == 1:
                self.clip_bottom = 0
            elif self.uc.face_dir == -1:
                self.clip_bottom = 2
        else:
            if right_down(e) or left_up(e):
                self.uc.delta_move = self.uc.face_dir = 1
                self.clip_bottom = 0
            elif left_down(e) or right_up(e):
                self.uc.delta_move = self.uc.face_dir = -1
                self.clip_bottom = 2

    def exit(self, e):
        self.uc.frame = 0

    def do(self):
        dt = min(game_framework.frame_time, 0.06)
        self.uc.frame = (self.uc.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME_RUN * dt) % 6
        self.uc.x += self.uc.delta_move * RUN_SPEED_PPS * dt

        if self.uc.face_dir == 1 and int(self.uc.frame) >= 6:
            self.clip_bottom = 1
            self.uc.frame -= 6
        elif self.uc.face_dir == -1 and int(self.uc.frame) >= 6:
            self.clip_bottom = 3
            self.uc.frame -= 6

    def draw(self):
        self.image.clip_draw(
            int(self.uc.frame) * self.clip_width, self.clip_bottom * self.clip_height,
            self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
        )

class Idle:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_idle_sprite_sheet.png')
        file_path = '2DGP_attack/'
        self.attack_image_R = load_image(file_path + 'uc_attack_R.png')
        self.attack_image_L = load_image(file_path + 'uc_attack_L.png')
        self.attack_image_effect = load_image(file_path + 'uc_bullet_effect.png')
        self.clip_width = 402
        self.clip_height = 382
        self.clip_bottom = 0

    def enter(self, e):
        self.uc.delta_move = 0
        self.uc.frame = 0
        self.uc.is_moving = False

    def exit(self, e):
        if space_down(e):
            self.uc.attack()

    def do(self):
        pass

    def draw(self):
        if self.uc.is_attacking and (get_time() - self.uc.attack_time) < ATTACK_DURATION:
            effect_loc_x = 60 * self.uc.face_dir
            effect_loc_y = 15
            if self.uc.face_dir == 1:
                self.attack_image_R.draw(self.uc.x, self.uc.y, 300, 300)
                self.attack_image_effect.draw(self.uc.x + effect_loc_x, self.uc.y + effect_loc_y, 80, 80)
            else:
                self.attack_image_R.composite_draw(0, 'h', self.uc.x, self.uc.y, 300, 300)
                self.attack_image_effect.draw(self.uc.x + effect_loc_x, self.uc.y + effect_loc_y, 80, 80)
        else:
            if self.uc.is_attacking and (get_time() - self.uc.attack_time) >= ATTACK_DURATION:
                self.uc.is_attacking = False
            if self.uc.face_dir == 1:  # right
                self.image.clip_draw(
                    3 * self.clip_width, self.clip_bottom * self.clip_height,
                    self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
                )
            else:  # face_dir == -1: # left
                self.image.clip_composite_draw(
                    3 * self.clip_width, self.clip_bottom * self.clip_height,
                    self.clip_width, self.clip_height, 0, 'h', self.uc.x, self.uc.y, 300, 300
                )


class UserChar:
    def __init__(self, x, y):
        self.hp = 100
        self.x, self.y = x, y
        self.frame = 0
        self.face_dir = 1 # 1: right, -1: left
        self.delta_move = 0
        self.is_moving = False
        self.is_attacking = False
        self.is_defending = False
        self.is_down = False
        self.is_dead = False

        self.hp_empty_bar = load_image("2DGP_GUI/player_hp_empty.png")
        self.hp_bar = load_image("2DGP_GUI/player_hp.png")
        # self.bar_image_size_x = 1211
        # self.bar_image_size_y = 101
        self.bar_center_x = 500
        self.bar_center_y = 900
        self.curr_bar_center_x = 500
        self.curr_bar_center_y = 900
        self.max_bar_size_x = 500
        self.max_bar_size_y = 30
        self.curr_bar_size_x =  self.max_bar_size_x
        self.curr_bar_size_y = self.max_bar_size_y

        self.face_image = load_image("2DGP_GUI/uc_face_in_game.png")
        self.face_image_rate = 560 / 562

        self.font = load_font('ENCR10B.TTF', 16)

        # 공격 시작 시각 기록
        self.attack_time = 0.0

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.DOWN_RUN = DownRun(self)
        self.DOWN_IDLE = DownIdle(self)
        self.DEFEND_RUN = DefendRun(self)
        self.DEFEND_IDLE = DefendIdle(self)
        self.DEATH = Death(self)

        self.STATE_MACHINE = StateMachine(
            self.IDLE,  # 시작상태
            {  # 룰
                self.IDLE: {hp_depleted: self.DEATH, q_down: self.DEFEND_IDLE, down_down: self.DOWN_IDLE, space_down: self.IDLE,
                            right_up: self.RUN, left_up: self.RUN, right_down: self.RUN, left_down: self.RUN},
                self.RUN: {hp_depleted: self.DEATH, q_down: self.DEFEND_RUN, down_down: self.DOWN_RUN,
                           right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE},
                self.DOWN_IDLE: {hp_depleted: self.DEATH, down_up: self.IDLE, right_up: self.DOWN_RUN, left_up: self.DOWN_RUN,
                                 right_down: self.DOWN_RUN, left_down: self.DOWN_RUN},
                self.DOWN_RUN: {hp_depleted: self.DEATH, down_up: self.RUN, right_up: self.DOWN_IDLE, left_up: self.DOWN_IDLE,
                                 right_down: self.DOWN_IDLE, left_down: self.DOWN_IDLE},
                self.DEFEND_IDLE: {hp_depleted: self.DEATH, q_up: self.IDLE, right_up: self.DEFEND_RUN, left_up: self.DEFEND_RUN,
                                 right_down: self.DEFEND_RUN, left_down: self.DEFEND_RUN},
                self.DEFEND_RUN: {hp_depleted: self.DEATH, q_up: self.RUN, right_up: self.DEFEND_IDLE, left_up: self.DEFEND_IDLE,
                                 right_down: self.DEFEND_IDLE, left_down: self.DEFEND_IDLE},
                self.DEATH: {} # 죽음 상태에서는 아무 이벤트도 처리하지 않음
            }
        )

    def update(self):
        if self.is_dead:
            game_world.remove_object(self)
        self.STATE_MACHINE.update()
        self.curr_bar_size_x = 5 * self.hp
        self.curr_bar_center_x = (self.bar_center_x - (self.max_bar_size_x / 2)) + (self.curr_bar_size_x / 2)

    def draw(self):
        self.STATE_MACHINE.draw()
        self.hp_empty_bar.draw(self.bar_center_x, self.bar_center_y, self.max_bar_size_x, self.max_bar_size_y)
        self.hp_bar.draw(self.curr_bar_center_x, self.curr_bar_center_y, self.curr_bar_size_x, self.curr_bar_size_y)
        self.face_image.composite_draw(0, 'h', 150, 900, 200, 200 * self.face_image_rate)
        #self.hp_bar.clip_draw(0, 0, self.bar_image_size_x, self.bar_image_size_y, self.curr_bar_center_x, self.curr_bar_center_y, self.curr_bar_size_x, self.curr_bar_size_y)
        #self.font.draw(self.x - 40, self.y + 100, f'Hp {self.hp:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.STATE_MACHINE.handle_state_event(('INPUT', event))

    def attack(self):
        # 플래그와 시작 시각을 기록
        self.is_attacking = True
        self.attack_time = get_time()
        print('attack')
        loc_x = 55 * self.face_dir
        loc_y = 20
        bullet = Bullet(self.x + loc_x, self.y + loc_y, self.face_dir * 20)
        game_world.add_object(bullet, 1)
        game_world.add_collision_pair('basic:bullet', None, bullet)
        game_world.add_collision_pair('boss:bullet', None, bullet)

    def get_bb(self):
        if self.is_down:
            return self.x - 90, self.y - 140, self.x + 90, self.y - 50
        else:
            return self.x - 40, self.y - 100, self.x + 40, self.y + 100

    def handle_collision(self, group, other):
        if group == 'uc:fire':
            damage = 10
            if self.is_defending:
                damage = damage // 2
            self.hp -= damage
            print('uc:fire collision')
            print(f'User Character HP: {self.hp}')
            if self.hp <= 0:
                self.STATE_MACHINE.handle_state_event(('HP', 'DEATH'))
        elif group == 'uc:slash':
            damage = 20
            if self.is_defending:
                damage = damage // 2
            self.hp -= damage
            print('uc:slash collision')
            print(f'User Character HP: {self.hp}')
            if self.hp <= 0:
                self.STATE_MACHINE.handle_state_event(('HP', 'DEATH'))