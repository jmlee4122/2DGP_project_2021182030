from pico2d import load_image, delay
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_a, SDLK_SPACE

import game_world
from bullet import Bullet
from state_machine import StateMachine

def is_randed(e):
    return e[0] == 'RANDED'
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def upward_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

class Death:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_death_sprite_sheet.png')
        self.clip_width = 402
        self.clip_height = 382

    def enter(self, e):
        self.uc.frame = 0
        self.uc.is_jumping = False
        self.uc.is_moving = False
        self.uc.y = 400

    def exit(self, e):
        pass

    def do(self):
        if self.uc.frame == 8:
            self.uc.frame = 7
        self.uc.frame += 1
        pass

    def draw(self):
        if self.uc.face_dir == 1:
            self.image.clip_draw(
                (self.uc.frame - 1) * self.clip_width, 0, self.clip_width, self.clip_height,
                self.uc.x, self.uc.y, 300, 300
            )
        else:
            self.image.clip_composite_draw(
                (self.uc.frame - 1) * self.clip_width, 0, self.clip_width, self.clip_height,
                0, 'h', self.uc.x, self.uc.y, 300, 300
            )

class Jump:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_jump_sprite_sheet.png')
        self.clip_width = 546
        self.clip_height = 490
        self.frame = 0

    def enter(self, e):
        self.frame = 0
        self.uc.is_jumping = True
        print('enter Jump')

    def exit(self, e):
        self.uc.frame = 0
        self.uc.is_jumping = False

    def do(self):
        if self.frame == 6:
            self.uc.STATE_MACHINE.handle_state_event(('RANDED', None))
        else:
            self.frame += 1
            self.uc.x += self.uc.delta_move * 20
            self.uc.y = 400 + (-30 * (self.frame - 1) * (self.frame - 1 - 5))

    def draw(self):
        if self.uc.face_dir == 1:
            self.image.clip_draw(
                (self.frame - 1) * self.clip_width, 0, self.clip_width, self.clip_height,
                self.uc.x, self.uc.y, 300 * (490 / 382), 300 * (490 / 382)
            )
        else:
            self.image.clip_composite_draw(
                (self.frame - 1) * self.clip_width, 0, self.clip_width, self.clip_height,
                0, 'h', self.uc.x, self.uc.y, 300 * (490 / 382), 300 * (490 / 382)
            )
        delay(0.01)



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
        self.frame = 0

    def enter(self, e):
        self.uc.frame = 0
        self.uc.is_moving = True
        if right_down(e) or left_up(e):
            self.uc.delta_move = self.uc.face_dir = 1
            self.clip_bottom = 0
        elif left_down(e) or right_up(e):
            self.uc.delta_move = self.uc.face_dir = -1
            self.clip_bottom = 2

    def exit(self, e):
        if space_down(e):
            self.uc.attack()
            self.uc.is_attacking = True

    def do(self):
        self.uc.frame = (self.uc.frame + 1) % 12
        self.frame = self.uc.frame
        self.uc.x += self.uc.delta_move * 8

        if self.uc.face_dir == 1 and self.uc.frame >= 6:
            self.clip_bottom = 1
            self.frame -= 6
        elif self.uc.face_dir == -1 and self.uc.frame >= 6:
            self.clip_bottom = 3
            self.frame -= 6

    def draw(self):
        if self.uc.is_attacking:
            if self.uc.face_dir == 1:
                self.attack_image_R.draw(self.uc.x, self.uc.y, 300, 300)
            else:
                self.attack_image_L.draw(self.uc.x, self.uc.y, 300, 300)
            self.uc.is_attacking = False
        else:
            self.image.clip_draw(
                self.frame * self.clip_width, self.clip_bottom * self.clip_height,
                self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
            )
            delay(0.01)

class Idle:
    def __init__(self, user_character):
        self.uc = user_character
        file_path = '2DGP_character/user_character/'
        self.image = load_image(file_path + 'user_idle_sprite_sheet.png')
        file_path = '2DGP_attack/'
        self.attack_image_R = load_image(file_path + 'uc_attack_R.png')
        self.attack_image_L = load_image(file_path + 'uc_attack_L.png')
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
            self.uc.is_attacking = True

    def do(self):
        pass

    def draw(self):
        if self.uc.is_attacking:
            if self.uc.face_dir == 1:
                self.attack_image_R.draw(self.uc.x, self.uc.y, 300, 300)
            else:
                self.attack_image_L.draw(self.uc.x, self.uc.y, 300, 300)
            self.uc.is_attacking = False
        else:
            if self.uc.face_dir == 1:  # right
                self.image.clip_draw(
                    3 * self.clip_width, self.clip_bottom * self.clip_height,
                    self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
                )
            else:  # face_dir == -1: # left
                self.image.clip_draw(
                    0 * self.clip_width, self.clip_bottom * self.clip_height,
                    self.clip_width, self.clip_height, self.uc.x, self.uc.y, 300, 300
                )


class UserChar:
    def __init__(self):
        self.x, self.y = 960, 400
        self.frame = 0
        self.face_dir = 1 # 1: right, -1: left
        self.delta_move = 0
        self.is_moving = False
        self.is_jumping = False
        self.is_attacking = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.DEATH = Death(self)
        self.STATE_MACHINE = StateMachine(
            self.IDLE,  # 시작상태
            {  # 룰
                self.IDLE: {space_down: self.IDLE, a_down: self.DEATH, upward_down: self.JUMP,
                            right_up: self.RUN, left_up: self.RUN, right_down: self.RUN, left_down: self.RUN},
                self.RUN: {space_down: self.RUN, a_down: self.DEATH, upward_down: self.JUMP,
                           right_down: self.IDLE, left_down: self.IDLE, right_up: self.IDLE, left_up: self.IDLE},
                self.JUMP: {space_down: self.JUMP, a_down: self.DEATH,
                            (lambda e: is_randed(e) and self.is_moving): self.RUN,
                            (lambda e: is_randed(e) and not self.is_moving): self.IDLE},
                self.DEATH: {} # 죽음 상태에서는 아무 이벤트도 처리하지 않음
            }
        )

    def update(self):
        self.STATE_MACHINE.update()

    def draw(self):
        self.STATE_MACHINE.draw()

    def handle_event(self, event):
        if self.is_jumping:
            self.jump_handle_event(event)
        else:
            self.STATE_MACHINE.handle_state_event(('INPUT', event))

    def jump_handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            self.STATE_MACHINE.handle_state_event(('INPUT', event))
            return
        if self.is_jumping and self.is_moving:  # 이동 점프
            if event.type == SDL_KEYDOWN:  # 이동 점프 중간에 반대 방향키가 눌린 경우
                if event.key == SDLK_RIGHT:
                    self.delta_move = 0
                    self.face_dir = 1
                    self.is_moving = False
                elif event.key == SDLK_LEFT:
                    self.delta_move = 0
                    self.face_dir = -1
                    self.is_moving = False
            elif event.type == SDL_KEYUP:  # 이동 점프 중간에 이동 방향키가 떼어진 경우
                if event.key == SDLK_RIGHT:
                    self.delta_move = 0
                    self.face_dir = 1
                    self.is_moving = False
                elif event.key == SDLK_LEFT:
                    self.delta_move = 0
                    self.face_dir = -1
                    self.is_moving = False
        elif self.is_jumping and not self.is_moving:  # 제자리 점프
            if event.type == SDL_KEYDOWN:  # 제자리 점프 중간에 방향키가 눌린 경우
                if event.key == SDLK_RIGHT:
                    self.delta_move = 1
                    self.face_dir = 1
                    self.is_moving = True
                elif event.key == SDLK_LEFT:
                    self.delta_move = -1
                    self.face_dir = -1
                    self.is_moving = True
            elif event.type == SDL_KEYUP:  # 제자리 점프 중간에 방향키가 떼어진 경우
                if event.key == SDLK_RIGHT:
                    self.delta_move = -1
                    self.face_dir = -1
                    self.is_moving = True
                elif event.key == SDLK_LEFT:
                    self.delta_move = 1
                    self.face_dir = 1
                    self.is_moving = True

    def attack(self):
        print('attack')
        loc_x = 55 * self.face_dir
        loc_y = 20
        bullet = Bullet(self.x + loc_x, self.y + loc_y, self.face_dir * 20)
        game_world.add_object(bullet, 1)